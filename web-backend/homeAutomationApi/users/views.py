### Rest Framework imports ###
from tempfile import TemporaryFile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, response, parsers, mixins
##Custom Code imports ###
from .serializers import user_serializer, allowed_person_serializer
from .models import custom_profile, allowed_person, household

from django.contrib.auth.models import User
from django.db.models import Q


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['household'] = user.household.id
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
    
class user_list(generics.GenericAPIView):
    model = custom_profile
    queryset = custom_profile.objects.all()
    
    def post(self, request, *args, **kwargs):
        data = self.request.data
        count = custom_profile.objects.filter(Q(username = data['username']) | Q(email = data['email'])).count()
        print(data)
        if(count > 0):  
            return response.Response('Username or email taken', status = 400)
        serializer = user_serializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status = 201)
        return response.Response("Error signing up", status = 400)        
            

class allowed_persons_list(generics.ListCreateAPIView):
    serializer_class = allowed_person_serializer
    model = allowed_person
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    
    def get_queryset(self):
        try:
            household = self.kwargs['household_id']
        except:
            return allowed_person.objects.none()
        
        try:
            qs = allowed_person.objects.filter(household__id=household)
        except:
            qs = allowed_person.objects.none()
            
        return qs
    

class allowed_persons_detail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'   
    queryset = allowed_person.objects.all()
    serializer_class = allowed_person_serializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
            

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs) 
    
    
#for home servers initial setup, return lists of both allowed
#and high alert persons
class allowed_high_alert_list(generics.GenericAPIView):
    serializer_class = allowed_person_serializer
    def get(self, *args, **kwargs):
        household = self.kwargs['household_id']
        allowed_query = allowed_person.objects.filter(household__pk = household)
        print(len(allowed_query))
        allowed_persons = allowed_person_serializer(allowed_query, many=True).data
        
        return response.Response({'allowed':allowed_persons}, status = 200
                                 )
    

    


