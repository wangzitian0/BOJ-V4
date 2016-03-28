from django.conf.urls import include, url
import ojuser.views


urlpatterns = [
    url(r"^signup/$", ojuser.views.OjUserSignupView.as_view(), name="account_signup"),
    url(r"^settings/$", ojuser.views.OjUserSettingsView.as_view(), name="account_settings"),
    url(r"^profiles/$", ojuser.views.OjUserProfilesView.as_view(), name="account_profiles"),
    url(r"^", include("account.urls")),
]
