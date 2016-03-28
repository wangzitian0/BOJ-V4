from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r"^signup/$", views.OjUserSignupView.as_view(), name="account_signup"),
    url(r"^settings/$", views.OjUserSettingsView.as_view(), name="account_settings"),
    url(r"^profiles/$", views.OjUserProfilesView.as_view(), name="account_profiles"),
    url(r"^", include("account.urls")),
]
