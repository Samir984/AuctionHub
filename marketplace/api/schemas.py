from ninja import Schema
from decimal import Decimal
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
    auction_price: Decimal
    start_time: datetime
    end_time: datetime

   

class BidSchema(Schema):
    id: int
    auction: int
    bidder_id: int 
    bid_amount: Decimal
    created_at: datetime

  