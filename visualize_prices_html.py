from sqlalchemy.orm import Session
from sqlalchemy import func, text
from db import engine
from model import Ticket, ArticlePrice
from extract import extract_lidl, extract_systeme_u, temp_path
from typing import List
from airium import Airium
import datetime


with Session(engine) as session:
    cnt = session.query(func.count().label("c"), ArticlePrice.article_name).select_from(
        ArticlePrice).group_by(ArticlePrice.article_name).cte()

    intersting_articles = session.query(cnt.c.article_name).filter(cnt.c.c > 2).order_by(cnt.c.c.desc()).all()

    forbidden_list = ['Poire', 'Tomate', 'Nectarine', 'Jambon sup']

    intersting_articles = [it[0] for it in intersting_articles]

    for forbiden in forbidden_list:
        intersting_articles = [article for article in intersting_articles if forbiden.upper() not in article]
    

    last_price = session.query(ArticlePrice.article_name, ArticlePrice.price, func.max(Ticket.date).label('date'))\
        .select_from(ArticlePrice)\
        .join(Ticket, Ticket.id == ArticlePrice.ticket_id)\
        .group_by(ArticlePrice.article_name)\
        .cte(name="last_price")
    
    min_price = session.query(ArticlePrice.article_name, func.min(ArticlePrice.price).label('price'), Ticket.date)\
        .select_from(ArticlePrice)\
        .join(Ticket, Ticket.id == ArticlePrice.ticket_id)\
        .group_by(ArticlePrice.article_name)\
        .cte(name="min_price")

    max_price = session.query(ArticlePrice.article_name, func.max(ArticlePrice.price).label('price'), Ticket.date)\
        .select_from(ArticlePrice)\
        .join(Ticket, Ticket.id == ArticlePrice.ticket_id)\
        .group_by(ArticlePrice.article_name)\
        .cte(name="max_price")
    
    last_6m_price = session.query(ArticlePrice.article_name, ArticlePrice.price, func.max(Ticket.date).label('date'))\
        .select_from(ArticlePrice)\
        .join(Ticket, Ticket.id == ArticlePrice.ticket_id)\
        .group_by(ArticlePrice.article_name)\
        .filter(Ticket.date < datetime.datetime.now() - datetime.timedelta(days=6*30))\
        .cte(name="last_6m_price")
    
    last_y_price = session.query(ArticlePrice.article_name, ArticlePrice.price, func.max(Ticket.date).label('date'))\
        .select_from(ArticlePrice)\
        .join(Ticket, Ticket.id == ArticlePrice.ticket_id)\
        .group_by(ArticlePrice.article_name)\
        .filter(Ticket.date < datetime.datetime.now() - datetime.timedelta(days=365))\
        .cte(name="last_y_price")
    
    infos = session.query(
        func.distinct(ArticlePrice.article_name), 
        last_price.c.price.label('last_price'),
        last_price.c.date.label('last_price_date'),
        last_6m_price.c.price.label('last_6m_price'),
        last_6m_price.c.date.label('last_6m_price_date'),
        last_y_price.c.price.label('max_price'),
        last_y_price.c.date.label('max_price_date'),
        )\
        .select_from(ArticlePrice)\
        .join(last_price, last_price.c.article_name == ArticlePrice.article_name)\
        .outerjoin(last_6m_price, last_6m_price.c.article_name == ArticlePrice.article_name)\
        .outerjoin(last_y_price, last_y_price.c.article_name == ArticlePrice.article_name)\
        .filter(ArticlePrice.article_name.in_(intersting_articles))

    # print(infos.all())

    a = Airium()
    # Generating HTML file
    a('<!DOCTYPE html>')
    with a.html(lang="fr"):
        with a.head():
            a.meta(charset="utf-8")
            a.title(_t="Synthèse des derniers prix relevés")
        with a.body():
            with a.h1():
                a("Synthèse des prix")
            with a.table():
                with a.thead():
                    with a.th():
                        a('Article')
                    with a.th():
                        a('Dernier prix')
                    with a.th():
                        a('Il y a 6 mois')
                    with a.th():
                        a('Il y a 1 an')
                with a.tbody():
                    for article_name, last_price, last_price_date, min_price, min_price_date, max_price, max_price_date in infos:
                        with a.tr():
                            with a.td():
                                a(article_name)
                            with a.td():
                                a(last_price)
                            with a.td():
                                a(min_price)
                            with a.td():
                                a(max_price)


    

    # Casting the file to a string to extract the value
    html = str(a)
    # Casting the file to UTF-8 encoded bytes:
    with open('report.html', 'w+') as report:
        report.write(str(a))