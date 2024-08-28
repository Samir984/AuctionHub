from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    owner: User  
   

    class Config:
        orm_mode = True

class AuctionSchema(BaseModel):
    id: int
    item: int
    owner: int  
    auction_price: float
    start_time: datetime
    end_time: datetime

    class Config:
        orm_mode = True

class BidSchema(BaseModel):
    id: int
    auction: int
    bidder_id: int 
    bid_amount: float
    created_at: datetime

    class Config:
        orm_mode = True
