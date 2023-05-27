from sqlalchemy.orm import Session
from db import engine
from model import Ticket, ArticlePrice
from extract import extract_lidl, extract_systeme_u, temp_path
from typing import List

with Session(engine) as session:
    # Cleanup
    session.query(ArticlePrice).delete()
    session.query(Ticket).delete()
    # 
    tickets: List[Ticket] = []
    tickets += extract_systeme_u(temp_path/"u")
    tickets += extract_lidl(temp_path/"lidl")
    for ticket in tickets:
        for article in ticket.prices:
            if article.article_name is None:
                print(f"Issue in ticket {ticket}, {article} has no name")

    categories = { article.article_name : article.category for ticket in tickets for article in ticket.prices if article.category is not None}
    for ticket in tickets:
        for article in ticket.prices:
            if article.article_name in categories:
                article.category = categories[article.article_name]
    # print(tickets)
    session.add_all(tickets)
    session.commit()
    print(f"{session.query(Ticket).count()} tickets stored (with {session.query(ArticlePrice).count()} prices)")
