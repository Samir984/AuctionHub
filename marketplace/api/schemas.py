from ninja import Schema
from typing import Optional
from datetime import datetime
from django.contrib.auth.models import User
from .models import Item,Bid,Auction


class ItemSchema(Schema):
    id: int
    name: str
    description: str
    created_at: datetime
    # owner:User
  



class AuctionSchema(Schema):
    id: int
    item: int
    owner: int  
    auction_price: float
    start_time: datetime
    end_time: datetime

   

class BidSchema(Schema):
    id: int
    auction: int
    bidder_id: int 
    bid_amount: float
    created_at: datetime

  