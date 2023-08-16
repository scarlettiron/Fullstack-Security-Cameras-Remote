
### not currently in use ###
class ip_address_access_verification():
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.method ==  "GET":
            client_ip = request.META['REMOTE_ADDR']
            print(client_ip)
        
        
        response = self.get_response(request)
        return response