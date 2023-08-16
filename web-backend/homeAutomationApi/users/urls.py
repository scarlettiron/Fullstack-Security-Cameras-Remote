from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views as v

urlpatterns = [
    path('token/', v.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('list-create/', v.user_list.as_view(), name="user-list-create"),
    path('allowed-persons/list/<int:household_id>/', v.allowed_persons_list.as_view(), name='allowed_persons_list'),
    path('allowed-persons/detail/<int:pk>/', v.allowed_persons_detail.as_view(), name="allowed_persons_detail"),
    path('face-rec-list/<int:household_id>/', v.allowed_high_alert_list.as_view(), name = 'face-rec-list'),
]