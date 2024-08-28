from ninja import Schema
from datetime import datetime
from decimal import Decimal

class ItemSchema(Schema):
    id: int
    name: str
    image:str
    description: str
    starting_price: Decimal
    created_at: datetime
    owner_id: int

class AuctionSchema(Schema):
    id: int
    item: ItemSchema
    start_time: datetime
    end_time: datetime

class BidSchema(Schema):
    id: int
    auction_id: int
    bidder_id: int
    bid_amount: Decimal
    bid_time: datetime
