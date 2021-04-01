from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from django.utils.translation import ugettext_lazy as _
# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView

from users.forms import UserRegisterForm, StaffCreationForm
from users.models import Staff, Guest


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        staff_form = StaffCreationForm(request.POST, request.FILES)
        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save()
            user.is_staff = True
            user.save()
            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            messages.success(request, f'Account created for {username} !!')
            group = Group.objects.get(name='Staff')
            user.groups.add(group)
            return redirect('/')
    else:
        user_form = UserRegisterForm()
        staff_form = StaffCreationForm()
    context = {
        'user_form': user_form,
        'staff_form': staff_form
    }
    return render(request, 'users/register.html', context)


class StaffListView(ListView):
    model = Staff
    context_object_name = 'staffs'
    template_name = 'users.staff_list.html'
    ordering = 'staff_id'


class StaffDetailView(DetailView):
    model = Staff
    template_name = 'users/staff_detail.html'


class GuestListView(ListView):
    model = Guest
    paginate_by = 5
    allow_empty = True
    queryset = Guest.objects.all().filter(Q(reservation__checkin__isnull=False),
                                             Q(reservation__checkin__checkout__isnull=True))
    template_name = 'users/guest_list.html'
    context_object_name = 'guest_list'


class GuestDetailView(DetailView):
    model = Guest
    title = _("Customer Information")
    raise_exception = True


class ProfileView(TemplateView):
    template_name = 'users/profile.html'
    title = "Profile"
    extra_context = {'title': title}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['information'] = get_object_or_404(Staff, user=self.request.user)
            context['user_information'] = self.request.user
        else:
            raise Http404("Your are not logged in.")
        return context