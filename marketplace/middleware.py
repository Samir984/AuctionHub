import time


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
        print(start_time,time.time())
        print(f"\n{'=' * 30}\nResponse Processed\n")
        print(f"Status Code: {response.status_code}")
        print(f"Time Taken: {duration:.4f} seconds\n")

        return response
