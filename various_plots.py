from sqlalchemy.orm import Session
from sqlalchemy import func
from db import engine
from model import Ticket, ArticlePrice
from extract import extract_lidl, extract_systeme_u, temp_path
from typing import List
from matplotlib import pyplot
from itertools import groupby, cycle


with Session(engine) as session:
    cnt = session.query(func.count().label("c"), ArticlePrice.article_name).select_from(
        ArticlePrice).group_by(ArticlePrice.article_name).cte()

    intersting_articles = session.query(cnt.c.article_name).filter(cnt.c.c > 4).order_by(cnt.c.c.desc()).all()

    forbidden_list = ['Poire', 'Tomate', 'Nectarine', 'Jambon sup']

    intersting_articles = [it[0] for it in intersting_articles]

    for forbiden in forbidden_list:
        intersting_articles = [article for article in intersting_articles if forbiden.upper() not in article]

    price_evolutions = session.query(Ticket.date, ArticlePrice.price, ArticlePrice.article_name)\
        .select_from(ArticlePrice)\
        .join(Ticket, ArticlePrice.ticket_id == Ticket.id)\
        .filter(ArticlePrice.article_name.in_(intersting_articles), Ticket.store_name == "U")\
        .order_by(ArticlePrice.article_name.asc(), Ticket.date.asc())\
        .all()

    print(len(price_evolutions))
    groups = groupby(price_evolutions, lambda x: x[2])
    # print(len(list(groups)))

    # for article_name, article_prices in groups:
    #     prices = list(article_prices)
    #     if len(prices) <=1:
    #         continue
    #     print(f"{article_name=} {(prices)}")

    fig, ax = pyplot.subplots()
    fig.set_size_inches( 11, 8)
    marker = cycle((',', '+', '.', 'o')) 


    for article_name, article_prices in groups:
        prices = list(article_prices)
        if len(prices) <= 1:
            continue
        # print(f"{article_name=} {(prices)}")
        print(f"{article_name=}", [it[0] for it in prices], [it[1] for it in prices])
        pyplot.plot([it[0] for it in prices], [it[1] for it in prices], label=article_name, marker= next(marker))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height*0.8])
    pyplot.legend(fontsize="xx-small", ncols=4, loc="upper right", bbox_to_anchor=(1, 1.35))
    pyplot.savefig('plot.png')
    # pyplot.show()
