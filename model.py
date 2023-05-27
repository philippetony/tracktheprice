from dataclasses import dataclass, field
from datetime import date
from typing import List
from sqlalchemy import String, Float, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_collection, mapped_column, relationship, Mapped


class Base(DeclarativeBase):
    pass


class ArticlePrice(Base):
    __tablename__ = 'article_price'
    id: Mapped[int] = mapped_column(primary_key=True)
    article_name: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column(Float())
    category: Mapped[str] = mapped_column(String(), nullable=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey('ticket.id'))

    @staticmethod
    def of(name, price, category = None):
        it = ArticlePrice()
        it.article_name = name
        it.price = price
        it.category = category
        return it
    
    def __repr__(self):
        return f"{self.article_name or '':<30}{self.price or '':>6}{self.category or '':<20}"


class Ticket(Base):
    __tablename__ = 'ticket'
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date] = mapped_column(Date())
    prices: Mapped[List['ArticlePrice']] = relationship()
    store_name: Mapped[str] = mapped_column(String())
    store_city: Mapped[str] = mapped_column(String())

    def __repr__(self):
        s = f"<{self.date}  {len(self.prices)} articles {round(sum([it.price for it in self.prices]),2)}€>"
        return s

    def __str__(self):
        s = f"Date: {self.date}\n"
        for item in self.prices:
            s += item.__repr__()+"\n"
        return s
