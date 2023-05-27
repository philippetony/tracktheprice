from sqlalchemy.orm import Session
from sqlalchemy import func
from db import engine
from model import Ticket, ArticlePrice
from extract import extract_lidl, extract_systeme_u, temp_path
from typing import List


with Session(engine) as session:
    print(f"{session.query(Ticket).count()} tickets stored")
    print(f"{session.query(ArticlePrice).count()} unitary prices")
    print(f"{session.query(ArticlePrice).group_by(ArticlePrice.article_name).count()} different articles")
    cnt = session.query(func.count().label("c"), ArticlePrice.article_name).select_from(
        ArticlePrice).group_by(ArticlePrice.article_name).cte()
    print(f"{session.query(func.max(cnt.c.c)).scalar()} max prices for a single article")
    print(f"{session.query(cnt).filter(cnt.c.c > 1).count()} items with 2 or more prices")

    print("Top 20 articles with most prices : "+'\n\t- '.join([f"{x[0]}  ({x[1]})" for x in session.query(
        cnt.c.article_name, cnt.c.c).filter(cnt.c.c > 1).order_by(cnt.c.c.desc()).limit(20).all()]))
