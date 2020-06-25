from django.urls import include, reverse_lazy
from django.conf.urls import re_path
from djangoadmin import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "djangoadmin"

urlpatterns = [
    # api-token views.
    re_path(r'^api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # normal views.
    re_path(r'^account/$', views.AccountView, name='account_view'),
    re_path(r'^profile/$', views.ProfileView, name='profile_view'),
    re_path(r'^profile/edit/$', views.EditProfileView, name="edit_profile_view"),
    re_path(r'^register/$', views.SignupView, name="signup_view"),
    re_path(r'^login/$', views.LoginView, name="login_view"),
    re_path(r'^password-change/$', views.PasswordChangeView, name="password_change_view"),
    re_path(r'^password-reset/$', auth_views.PasswordResetView.as_view(template_name="djangoadmin/djangoadmin/password_reset_view.html", email_template_name='djangoadmin/djangoadmin/password_reset_email.html', success_url=reverse_lazy('djangoadmin:password_reset_done')), name="password_reset"),
    re_path(r'^password-reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name="djangoadmin/djangoadmin/password_reset_done_view.html"), name="password_reset_done"),
    re_path(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(template_name="djangoadmin/djangoadmin/password_reset_confirm_view.html", success_url=reverse_lazy('djangoadmin:password_reset_complete')), name="password_reset_confirm"),
    re_path(r'^password-reset-complete/$', auth_views.PasswordResetCompleteView.as_view(template_name="djangoadmin/djangoadmin/password_reset_complete_view.html"), name="password_reset_complete"),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name="logout_view")
]