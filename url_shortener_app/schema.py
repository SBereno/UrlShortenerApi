from pydantic import BaseModel
from typing import Optional


class url_schema(BaseModel):
   key: Optional[str] = None
   target_url: str
   clicks: Optional[int] = None

   class Config:
       orm_mode = True
