from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.errors import HttpError
from django.utils import timezone
from .schemas import ItemSchema, AuctionSchema, BidSchema
from .models import Item, Auction, Bid
from datetime import datetime

api = NinjaAPI()


@api.get("")
def message(request):
    return "Djanjo Project api route"
  

@api.get("/items/", response=list[ItemSchema])
def list_items(request):
    items = Item.objects.all()
    return items

@api.get("/auctions/", response=list[AuctionSchema])
def list_auctions(request):
    auctions = Auction.objects.all()
    return auctions



@api.post("/auctions/", response=AuctionSchema)
def create_auction(request, item_id: int, auction_price: float, start_time: datetime, end_time: datetime):

    auction = Auction.objects.create(
        item_id,
        owner_id=request.user,
        auction_price=auction_price,
        start_time=start_time,
        end_time=end_time
    )
    
    return auction


@api.get("/bids/{auction_id}/", response=list[BidSchema])
def list_bids(request, auction_id: int):
    bids = Bid.objects.filter(auction_id=auction_id)
    return bids


@api.post("/bids/", response=BidSchema)
def create_bid(request, auction_id: int, bid_amount: float, bid_time: datetime):
    # Get the auction object
    auction = get_object_or_404(Auction, id=auction_id)

    # Check if the user trying to bid is the owner of the auction item
    if auction.item.owner == request.user:
        raise HttpError(400, "You cannot bid on your own auction.")
    
    # Check if the auction is active
    if not auction.is_active():
        raise HttpError(400, "Auction is not active")
    

    # Create the bid if the user is not the owner
    bid = Bid.objects.create(
        auction_id,
        bidder=request.user,
        bid_amount=bid_amount
    )

    # Transfer item ownership if the bid meets or exceeds a certain condition
    if bid_amount >= auction.auction_price:
     currentOwner=auction.item
     print(currentOwner)
    

    return {"id": bid.id, "message": "Bid created successfully."}
