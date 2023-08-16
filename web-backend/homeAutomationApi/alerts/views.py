from rest_framework import generics, authentication, permissions, response
from .serializers import alert_serializer, create_alert_serializer
from .models import alert
from .utils import find_device_pk


#supports single and multiple alert creation
class alert_list_create(generics.ListCreateAPIView):
    queryset = alert.objects.all().select_related('device')
    serializer_class = alert_serializer
    
    def get_serializer_class(self, *args, **kwars):
        if self.request.method == 'GET':
            return alert_serializer
        return create_alert_serializer
    
    def get_queryset(self):
        household = self.kwargs['household_id']
        try:
            qs = alert.objects.filter(device__household__id = household).select_related('device')
        except:
            qs = alert.objects.none()
            
        return qs

    def create(self, request, *args, **kwargs):
        data = self.request.data
        find_device_pk(data)
        if isinstance(data, list):
            serializer = create_alert_serializer(many=True, data=data, partial=True)
        else:
            serializer = create_alert_serializer(data = data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(status = 201)
        print('serializer not valid')
        return response.Response(status = 400)

    
 
    
class alert_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = alert.objects.all().select_related('device')
    serializer_class = alert_serializer
    
    
