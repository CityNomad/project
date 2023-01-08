from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from accounts.models import Profile
from webapp.forms import SearchForm


# Create your views here.\


class RegisterView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:home')
        return next_url


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webapp:home')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:home')


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "profile.html"
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.order_by("-start_date")
        return context


class ProfileListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = "users_list.html"
    context_object_name = "users"
    permission_required = 'webapp.view_list_of_users'
    ordering = "id"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return User.objects.filter(
                Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return User.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class ChangeProfileView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "change_user.html"
    profile_form_class = ProfileChangeForm
    context_object_name = "user_obj"

    def has_permission(self):
        return self.request.user.is_superuser or self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "profile_form" not in context:
            context["profile_form"] = self.profile_form_class(instance=self.get_object().profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        profile_form = self.profile_form_class(instance=self.object.profile,
                                               data=request.POST,
                                               files=request.FILES)
        if form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        # self.get_form()
        form.save()
        profile_form.save()
        return redirect("accounts:profile", self.object.pk)

    def form_invalid(self, form, profile_form):
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))


# class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
#     model = get_user_model()
#     template_name = 'change_password.html'
#     form_class = PasswordChangeForm
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def get_success_url(self):
#         return reverse('accounts:profile', kwargs={"pk": self.request.user.pk})
#
#     def form_valid(self, form):
#         result = super().form_valid(form)
#         update_session_auth_hash(self.request, self.object)
#         return result


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={"pk": self.request.user.pk})