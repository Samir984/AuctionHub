from ninja import NinjaAPI


api = NinjaAPI()


@api.get("")
def message(request):
    return "Djanjo Project api route"
  