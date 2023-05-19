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