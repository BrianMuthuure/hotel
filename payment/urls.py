from django.urls import path

from payment.views import CheckInListView, CheckInDetailView, CheckOutListView, CheckOutDetailView

urlpatterns = [
    path('check_ins/', CheckInListView.as_view(), name='check_in-list'),
    path('check_in/<str:pk>', CheckInDetailView.as_view(), name='check_in-detail'),
    path('check_outs/', CheckOutListView.as_view(), name='check_out-list'),
    path('check_out/<str:pk>', CheckOutDetailView.as_view(), name='check_out-detail'),
]