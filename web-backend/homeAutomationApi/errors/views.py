from requests import Response
from rest_framework import generics
from rest_framework.response import Response
from .models import error_log
from .serializers import error_log_serializer
from .utils import find_device_pk


class error_log_list(generics.ListCreateAPIView):
    model = error_log
    serializer_class = error_log_serializer
    queryset = error_log.objects.all()
    
    def get_queryset(self):
        household_id = self.kwargs['household_id']
        try:
            qs = error_log.objects.filter(device__household__id = household_id)
        except:
            qs = error_log.objects.none()
        return qs
    
    #takes a list of error logs submitted from local server
    def create(self, request, *args, **kwargs):
        #logs = request.GET.get('logs', None)
        data = self.request.data
        find_device_pk(data)
        
        if isinstance(data, list):
            serializer = error_log_serializer(data=data, many=True, partial=True)
        else:
            serializer = error_log_serializer(data=data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status = 201)
            


    
class error_log_detail(generics.RetrieveUpdateDestroyAPIView):
    model = error_log
    serializer_class = error_log_serializer
    queryset = error_log.objects.all()
    lookup_field = ['pk']
    
    
