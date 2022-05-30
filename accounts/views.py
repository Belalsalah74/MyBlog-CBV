from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from accounts.forms import ProfileCreateForm, UserUpdateForm
from .models import Profile

User = get_user_model()


class LogoutConfirm(TemplateView):    
    def get(self,request):
        return render(request, 'accounts/logout.html')

class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = '/'


class ProfileDetail(LoginRequiredMixin,DetailView):
    model = Profile


class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Profile
    form_class = ProfileCreateForm
    success_url = '/'
    
    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user:
            return True
        return False

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      profile = self.get_object()
      user = get_object_or_404(User, profile=profile)
      user_form = UserUpdateForm(instance=user)
      context["user_form"] = user_form
      return context
  

    def post(self,request,*args, **kwargs):
        profile = self.get_object()
        user = get_object_or_404(User,profile=profile)
        form = self.get_form()
        user_form = UserUpdateForm(request.POST, instance=user)
        print(user_form.is_valid())
        print(form.is_valid())
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            return super().post(self,*args, **kwargs)
        return render(request, 'accounts/profile_up date.html')
        
