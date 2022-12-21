from enum import unique
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text
import database


class Url(database.Base):
   __tablename__ = "Urls"
   id = Column(Integer, primary_key=True, index=True)
   key = Column(Text(), unique=True)
   target_url = Column(Text())
   clicks = Column(Integer, default=0)
