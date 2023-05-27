from sqlalchemy import create_engine
from model import Base

engine = create_engine("sqlite:///tracktheprice.db", echo=False)
Base.metadata.create_all(engine)