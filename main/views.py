from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView
from django.views.generic.edit import FormMixin

from main.forms import RoomCreationForm, RoomUpdateForm, ImageCreateForm, ReservationForm
from main.models import Room, RoomImage, Reservation
from payment.forms import CheckInRequestForm
from users.models import Guest, Staff


def home(request):

    total_num_rooms = Room.objects.all().count()
    available_num_rooms = Room.objects.exclude(reservation__isnull=False).count()
    total_num_reservations = Reservation.objects.all().count()
    total_num_staffs = Staff.objects.all().count()
    total_num_customers = Guest.objects.all().count()
    if total_num_reservations == 0:
        last_reserved_by = Reservation.objects.none()
    else:
        last_reserved_by = Reservation.objects.get_queryset().latest('date')

    return render(
        request,
        'main/home.html',
        {
            'total_num_rooms': total_num_rooms,
            'available_num_rooms': available_num_rooms,
            'total_num_reservations': total_num_reservations,
            'total_num_staffs': total_num_staffs,
            'total_num_customers': total_num_customers,
            'last_reserved_by': last_reserved_by,
        }
    )


class RoomListView(ListView):
    model = Room
    template_name = 'main/room_list.html'
    context_object_name = 'rooms'
    ordering = 'room_id'


class RoomCreationView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Room
    template_name = 'main/room_creation.html'
    form_class = RoomCreationForm
    success_message = 'room '

    def test_func(self):
        if self.request.user.is_admin:
            return True
        return False


class RoomDetailView(DetailView):
    model = Room
    template_name = 'main/room_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        context['photos'] = RoomImage.objects.filter(room=self.object)
        return context


class RoomUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Room
    template_name = 'main/room_update.html'
    form_class = RoomUpdateForm
    success_message = 'room was updated successfully'

    def test_func(self):
        if self.request.user.is_admin:
            return True
        return False


class RoomDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Room
    template_name = 'main/room_delete.html'
    success_url = reverse_lazy('room_list')

    def test_func(self):
        if self.request.user.is_admin:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        room = self.get_object()
        messages.success(request, f'Room %s was deleted successfully!!' % room.room_id)
        return super(RoomDeleteView, self).delete(request, *args, **kwargs)


class ImageCreateView(SuccessMessageMixin, CreateView):
    model = RoomImage
    form_class = ImageCreateForm
    template_name = 'main/image_form.html'
    success_message = 'image was added successfully'

    def get_initial(self):
        return {
            'room': self.kwargs['pk']
        }

    def get_success_url(self):
        return reverse('room_detail', kwargs={'pk': self.object.room.pk})


def add_image(request, pk):
    room = Room.objects.get(room_id=pk)
    form = ImageCreateForm(initial={'room': room})
    if request.method == 'POST':
        form = ImageCreateForm(request.POST or None, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'image added  successfully!')
            return HttpResponseRedirect(reverse('room_detail', kwargs={'pk': room.pk}))
    context = {'form': form}
    return render(request, 'main/image_form.html', context)


@transaction.atomic
def reserve(request):
    reservation = Reservation.objects.none()
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            try:
                with transaction.atomic():
                    guest = Guest(
                        first_name = reservation_form.cleaned_data.get('first_name'),
                        last_name = reservation_form.cleaned_data.get('last_name'),
                        email = reservation_form.cleaned_data.get('email'),
                        phone_no = reservation_form.cleaned_data.get('phone_no'),
                        gender = reservation_form.cleaned_data.get('gender'),
                        nationality = reservation_form.cleaned_data.get('nationality'),
                    )
                    guest.save()
                    reservation = Reservation(
                        guest = guest,
                        no_children = reservation_form.cleaned_data.get('no_children'),
                        no_adults = reservation_form.cleaned_data.get('no_adults'),
                        date = timezone.now(),
                    )
                    reservation.save()
                    for room in reservation_form.cleaned_data.get('rooms'):
                        room.reservation = reservation
                        room.save()
                        messages.success(request, f'reservation created successfully')
            except IntegrityError:
                raise Http404
            return redirect('/')
    else:
        reservation_form = ReservationForm()
    return render(request, 'main/reserve.html', {'reservation_form': reservation_form})


class ReservationListView(SuccessMessageMixin, ListView, FormView):
    model = Reservation
    paginate_by = 5
    allow_empty = True
    form_class = CheckInRequestForm
    success_url = reverse_lazy('reservations')
    success_message = 'guest was checked in successfully'

    def get_context_data(self, *args, **kwargs):
        context = super(ReservationListView, self).get_context_data(*args, **kwargs)
        return context

    def __init__(self, *args, **kwargs):
        super(ReservationListView, self).__init__(*args, **kwargs)
        self.object_list = self.get_queryset()

    @transaction.atomic
    def form_valid(self, form):
        try:
            with transaction.atomic():
                checkin = form.save(commit=False)
                checkin.user = self.request.user
                checkin.save()
        except IntegrityError:
            raise Http404
        return super().form_valid(form)


class ReservationDetailView(DetailView):
    model = Reservation
    raise_exception = True