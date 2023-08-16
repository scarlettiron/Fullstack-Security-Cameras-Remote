
from rest_framework import generics, response, mixins
from .models import device, device_passcode, local_server
from .serializers import device_serializer, device_passcodes_serializer, local_server_serialzer
from .mixins import device_mixin

class device_list_create(device_mixin, generics.ListCreateAPIView):
    queryset = device.objects.all().select_related('pair')
    serializer_class = device_serializer
    
    def get_queryset(self, *args, **kwargs):
        household = self.kwargs['household_pk']
        try:
            qs = device.objects.filter(household__id = household).select_related('pair')
        except:
            qs = device.objects.none()
        return qs
    
    def get(self, request, *args, **kwargs):
        household = self.kwargs['household_pk']
        modified_response = super().list(request, *args, **kwargs)
        try:
            server_qs = local_server.objects.filter(household__id = household)
            serializer = local_server_serialzer(server_qs, many=True).data
        except:
            serializer = []

        modified_response.data['servers'] = serializer
        return modified_response
        
class device_detail(device_mixin, generics.RetrieveAPIView, mixins.UpdateModelMixin):
    queryset = device.objects.all().select_related('pair')
    serializer_class = device_serializer
    lookup_field = 'pk'
    
    ''' def get_queryset(self):
        if self.request.method == 'PUT':
            try:
                print('getting qs')
                qs = device.objects.get(unit_id = self.kwargs['pk'])
            except:
                print('nope')
                qs = device.objects.none()
            return qs
        
        return super().get_queryset() '''
    
    #verify that device does not already belong to a household
    def put(self, request, *args, **kwargs):
        try:
            household = self.request.data['household']
        except:
            return super().partial_update(request, *args, **kwargs)
        try:
            unit = self.get_queryset()
        except:
            return super().partial_update(request, *args, **kwargs)
        
        if not unit:
            return response.Response( "unit not found" ,status = 404)
        
        if not unit[0].household:
            serializer = device_serializer(instance = unit, data=self.request.data, partial = True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response.Response(status=201)
        return response.Response('Device already belongs to a household', status=401)



#for user frontend
class device_passcodes(generics.DestroyAPIView):
    model = device_passcode
    queryset = device_passcode.objects.all()
    serializer_class = device_passcodes_serializer
    lookup_field = 'pk'
    
#create passcode on frontend
class create_device_passcode(generics.CreateAPIView):
    model = device_passcode
    queryset = device_passcode.objects.all()
    serializer_class = device_passcodes_serializer
    
    def post(self, request, *args, **kwargs):
        try:
            password_count = device_passcode.objects.filter(device__id = self.reguest.data['unit_id']).count()
            if password_count > 10:
                return response.Response('Maximum number of passwords allowed reached, delete a password in order to add another', status_code = 400)
        except:
                return response.Response("Error adding password", status = 400)
        
        return super().post(request, *args, **kwargs)


#hit by units for their corresponding passcodes   
class unit_pathway_device_passcodes(generics.ListAPIView):
    serializer_class = device_passcodes_serializer
    lookup_field = 'unit_id'
    queryset = device_passcode.objects.filter()
    
    def get_queryset(self):
        device_id = self.kwargs['unit_id']
        #client_ip = self.request.META['REMOTE_ADDR']
        #client_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', None)
        #if not client_ip:
        #    client_ip = self.request.META.get('REMOTE_ADDR', None)
            
        #print(client_ip)
        #keys = self.request.META.keys()
        #print(keys)
        try:
           # qs = device_passcode.objects.filter(device__ip_address = client_ip,
            #                                    device__unit_id = device_id)
            qs = device_passcode.objects.filter(device__id = device_id)
        except:
            qs = device_passcode.objects.none()
        return qs
    
    
    
class local_server_list(generics.ListAPIView):
    model = local_server
    serializer_class = local_server_serialzer
    
    def get_queryset(self):
        household = self.kwargs['household_id']
        try:
            qs = local_server.objects.filter(household__id = household)
        except:
                qs = local_server.objects.none()
        return qs

    
class local_server_detail(generics.RetrieveUpdateAPIView):
    model = local_server
    queryset = local_server.objects.all()
    lookup_field = 'unit_id'
    serializer_class = local_server_serialzer
    
    def put(self, request, *args, **kwargs):
        server = self.get_queryset()
        if self.request.data['household'] != self.request.user.household.pk:
            return response.Response('unauthorized!', status = 400)
        if not server[0].household:
            return self.partial_update(request, *args, **kwargs)
        return response.Response('This server already belongs to a household', status = 401)
            
    
    
