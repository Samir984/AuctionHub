from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from .schemas import ItemSchema, AuctionSchema, BidSchema
from .models import Item, Auction, Bid

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

@api.get("/bids/{auction_id}/", response=list[BidSchema])
def list_bids(request, auction_id: int):
    bids = Bid.objects.filter(auction_id=auction_id)
    return bids

@api.post("/bids/", response=BidSchema)
def create_bid(request, auction_id: int, bid_amount: float):
    auction = get_object_or_404(Auction, id=auction_id)
    bid = Bid.objects.create(auction=auction, bidder=request.user, bid_amount=bid_amount)
    return bid
