from django.db import transaction, IntegrityError
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView

from main.models import Facility
from payment.forms import CheckoutRequestForm
from payment.models import CheckIn, CheckOut
from users.models import Staff


class CheckInListView(ListView, FormView):
    model = CheckIn
    paginate_by = 5
    queryset = CheckIn.objects.all().order_by('-check_in_date_time')
    allow_empty = True
    permission_required = 'main.can_view_customer'
    title = "Check-In List"
    form_class = CheckoutRequestForm
    extra_context = {
        'title': title,
    }
    success_url = reverse_lazy('check_in-list')

    @transaction.atomic
    def form_valid(self, form):
        try:
            with transaction.atomic():
                checkout = form.save(commit=False)
                checkout.user = self.request.user
                checkout.save()
                for room in checkout.check_in.reservation.room_set.all():
                    room.reservation = None
                    room.save()
        except IntegrityError:
            raise Http404
        return super().form_valid(form)


class CheckInDetailView(DetailView):
    model = CheckIn
    num_facilities = Facility.objects.count()
    if not num_facilities:
        facilities = Facility.objects.none()
    else:
        facilities = Facility.objects.all()

    extra_context = {
        'facilities': facilities,
        'num_facilities': num_facilities,
    }

    def get_context_data(self, **kwargs):
        context = super(CheckInDetailView, self).get_context_data(**kwargs)
        checkin = context['checkin']
        rooms = checkin.rooms
        staff = Staff.objects.filter(user=checkin.user)
        if not staff.count():
            staff = Staff.objects.none()
        else:
            staff = Staff.objects.get(user=checkin.user)
        context['staff'] = staff
        if rooms:
            new_rooms = checkin.rooms.split(', ')
            new_rooms = list(map(str, new_rooms))
            context['rooms'] = new_rooms
        return context


class CheckOutListView(ListView):
    model = CheckOut
    paginate_by = 5


class CheckOutDetailView(DetailView):
    model = CheckOut

    def get_context_data(self, **kwargs):
        context = super(CheckOutDetailView, self).get_context_data(**kwargs)
        checkout = context['checkout']

        staff = Staff.objects.filter(user=checkout.user)
        if not staff.count():
            staff = Staff.objects.none()
        else:
            staff = Staff.objects.get(user=checkout.user)
        context['staff'] = staff

        return context