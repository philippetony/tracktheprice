from sqlalchemy.orm import Session
from sqlalchemy import func, text
from db import engine
from model import Ticket, ArticlePrice
from extract import extract_lidl, extract_systeme_u, temp_path
from typing import List
from airium import Airium
import datetime
import csv


with Session(engine) as session:
    with open("articles.csv", "w+") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['article_name','price','category','date', 'store_name', 'store_city'])
        for item in session.query(ArticlePrice.article_name, ArticlePrice.price, ArticlePrice.category, Ticket.date, Ticket.store_name, Ticket.store_city)\
            .select_from(ArticlePrice)\
            .join(Ticket, Ticket.id == ArticlePrice.ticket_id)\
            .all():
            writer.writerow(item)
