from sqlalchemy.orm import Session
from sqlalchemy import func
from db import engine
from model import Ticket, ArticlePrice
from extract import extract_lidl, extract_systeme_u, temp_path
from typing import List
from matplotlib import pyplot
from itertools import groupby, cycle
import re


with Session(engine) as session:
    cnt = session.query(func.count().label("c"), ArticlePrice.article_name).select_from(
        ArticlePrice).group_by(ArticlePrice.article_name).cte()

    intersting_articles = session.query(cnt.c.article_name).filter(cnt.c.c > 4).order_by(cnt.c.c.desc()).all()

    forbidden_list = ['Poire', 'Tomate', 'Nectarine', 'Jambon sup']

    intersting_articles = [it[0] for it in intersting_articles]

    for forbiden in forbidden_list:
        intersting_articles = [article for article in intersting_articles if forbiden.upper() not in article]

    price_evolutions = session.query(Ticket.date, ArticlePrice.price, ArticlePrice.article_name, ArticlePrice.category)\
        .select_from(ArticlePrice)\
        .join(Ticket, ArticlePrice.ticket_id == Ticket.id)\
        .filter(ArticlePrice.article_name.in_(intersting_articles), Ticket.store_name == "U")\
        .order_by(ArticlePrice.article_name.asc(), Ticket.date.asc())\
        .all()

    print(len(price_evolutions))
    categories = { price[2] : price[3] for price in price_evolutions if price[3] is not None}

    groups = {}
    for price in price_evolutions:
        article_name = price[2]
        category = categories[article_name] if article_name in categories else ''
        groups.setdefault(category, {})
        groups[category].setdefault(article_name, [])
        groups[category][article_name].append(price)


    # print(len(list(groups)))

    # for article_name, article_prices in groups:
    #     prices = list(article_prices)
    #     if len(prices) <=1:
    #         continue
    #     print(f"{article_name=} {(prices)}")


    
    for category, category_articles in groups.items():
        fig, ax = pyplot.subplots()
        fig.set_size_inches( 11, 8)
        marker = cycle((',', '+', '.', 'o')) 
        for article_name, article_prices in category_articles.items():
            prices = list(article_prices)
            print(prices)
            if len(prices) < 1:
                continue
            # print(f"{article_name=} {(prices)}")
            # print(f"{article_name=}", [it[0] for it in prices], [it[1] for it in prices])
            pyplot.plot([it[0] for it in prices], [it[1] for it in prices], label=article_name, marker= next(marker))

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height*0.8])
        pyplot.legend(fontsize="xx-small", ncols=4, loc="upper right", bbox_to_anchor=(1, 1.35))
        pyplot.savefig('plot%s.png' % ("_"+re.sub("[^\w ]+","_",category if category is not None else "")))
    # pyplot.show()
