from dataclasses import dataclass, field
from datetime import date
from typing import List

@dataclass
class ArticlePrice:
    article_name: str
    price: float

@dataclass
class Ticket:
    date: date = None
    prices: List[ArticlePrice] = field(default_factory = lambda: [])

    def __repr__(self):
        s = f"\nDate: {self.date}\n"
        for item in self.prices:
            s+=f"{item.article_name:<30}{item.price:>6}\n"
        return s