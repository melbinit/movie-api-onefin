from api.models import RequestsData

class RequestMiddlware():
    # Middleware to catch requests and log them to RequestsData model.
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        request_data = RequestsData(url=request.get_full_path())
        if request.user.is_authenticated:
            request_data.user = request.user
        request_data.save()
        return response
