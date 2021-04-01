from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import register, StaffListView, StaffDetailView, GuestListView, GuestDetailView, ProfileView

urlpatterns = [
    path('register/', register, name='register'),
    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff_detail'),
    path('guests/', GuestListView.as_view(), name='guest_list'),
    path('guest/<str:pk>', GuestDetailView.as_view(), name='guest_detail'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
]