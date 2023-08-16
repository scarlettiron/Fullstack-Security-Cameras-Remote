from . import views as v
from django.urls import path

urlpatterns = [
    path('list-create/<household_pk>/', v.device_list_create.as_view(), name="device-list-create"),
    path('detail/<int:pk>/', v.device_detail.as_view(), name='device-detail'),
    path('pw/create/', v.create_device_passcode.as_view(), name='create-pw'),
    path('pw/detail/<int:pk>/', v.device_passcodes.as_view(), name='pw-delete'),
    path('unit-pwd/<int:unit_id>/', v.unit_pathway_device_passcodes.as_view(), name="device-pwd"),
    path('local-server/list/<int:household_id>/', v.local_server_list.as_view(), name='local-server-list'),
    path('local-server/detail/<int:unit_id>/', v.local_server_detail.as_view(), name='local-server-detail'),
]