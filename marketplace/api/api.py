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
    return "Django Project API route"

@api.get("/items/", response=list[ItemSchema])
def list_items(request):
    items = Item.objects.all()
    print(items[0].owner.id)
    return items

@api.post("/items/", response=ItemSchema)
def create_item(request, name: str, description: str):
    # Creating an item with the owner's user ID
    print(name,description,request,request.user,"\n\n\n")
    item = Item.objects.create(
        owner=request.user,
        name=name,
        description=description,
    )
    return item

@api.get("/auctions/", response=list[AuctionSchema])
def list_auctions(request):
    auctions = Auction.objects.all()
    print(auctions[0].item.name,"\n\n\n\n")
    return auctions

@api.post("/auctions/", response=AuctionSchema)
def create_auction(request,item:int, auction_price: float, start_time: datetime, end_time: datetime):
    # Fetch the item to ensure it exists
    print(item,auction_price,start_time,end_time,"/n/n/n/n")
    item=get_object_or_404(Item,item=item)

    # Create an auction
    auction = Auction.objects.create(
        item=item,
        owner=request.user,
        auction_price=auction_price,
        start_time=start_time,
        end_time=end_time
    )
    return auction

@api.get("/bids/{auction_id}/", response=list[BidSchema])
def list_bids(request, auction_id: int):
    bids = Bid.objects.get(auction_id=auction_id)
    return bids



@api.post("/bids/", response=BidSchema)
def create_bid(request, auction_id: int, bid_amount: float, bid_time: datetime):
    # Get the auction object
    auction = get_object_or_404(Auction, id=auction_id)

    # Check if the user trying to bid is the owner of the auction item
    if auction.item_id.owner_id == request.user:
        raise HttpError(400, "You cannot bid on your own auction.")
    
    # Check if the auction is active
    if not auction.is_active():
        raise HttpError(400, "Auction is not active")
    
    # Create the bid if the user is not the owner
    bid = Bid.objects.create(
        auction_id=auction,
        bidder=request.user,
        bid_amount=bid_amount,
        created_at=bid_time
    )

    # Transfer item ownership if the bid meets or exceeds a certain condition
    if bid_amount >= auction.auction_price:
        auction.item_id.owner_id = request.user
        auction.item_id.save()

    return bid
