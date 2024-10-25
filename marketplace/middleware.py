import time
from django.http import HttpResponse


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view is called.
        print(f"\n{'=' * 30}\nProcessing Request...\n")
        print(f"Method: {request.method} | Path: {request.path}")
        start_time = time.time()  # Start timing

        # Get the response from the next middleware/view
        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        duration = time.time() - start_time  # Calculate duration
        # print(start_time, time.time())
        print(f"Status Code: {response.status_code}")
        print(f"Time Taken: {duration:.4f} seconds\n")
        print(f"\nResponse Processed\n{'=' * 30}\n")

        return response

    # def process_view(self, *args, **kwargs):
    #     print("before view this is execute\n")
    #     return None

    # def process_exception(self, request, exception):
    #     print(f"Execetion has occured \n\n\n\n",exception)
    #     return HttpResponse(exception)
