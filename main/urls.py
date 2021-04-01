from django.urls import path

from main.views import RoomListView, home, RoomDetailView, RoomCreationView, RoomUpdateView, RoomDeleteView, \
    add_image, reserve, ReservationListView, ReservationDetailView

urlpatterns = [
    path('', home, name='home'),
    path('create-room/', RoomCreationView.as_view(), name='room_create'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/<str:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('rooms/<str:pk>/update/', RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<str:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    path('add-image/<str:pk>/', add_image, name='add_image'),
    path('reserve/', reserve, name='reserve'),
    path('reservation/', ReservationListView.as_view(), name='reservations'),
    path('reservation/<str:pk>', ReservationDetailView.as_view(), name='reservation-detail'),
]