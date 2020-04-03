from .models import User
from .forms import UserForm
from django.views.generic import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


class ProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/profile.html'
    success_url = '/user/profile/'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["documents"] =
        return context
