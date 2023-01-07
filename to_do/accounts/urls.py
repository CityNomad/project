from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import login_view, logout_view, RegisterView, ProfileView, ProfileListView, ChangeProfileView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('registration/', RegisterView.as_view(), name="registration"),
    path("<int:pk>/", ProfileView.as_view(), name="profile"),
    path('users/', ProfileListView.as_view(), name='users'),
    path('<int:pk>/change/', ChangeProfileView.as_view(), name="change_profile"),
]