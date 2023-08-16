from django.urls import path
from . import views as v

urlpatterns = [
    path('list/<int:household_id>/', v.alert_list_create.as_view(), name='alert-list'),
    path('detail', v.alert_detail.as_view(), name='alert-detail'),
]
