from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
import ojuser.views

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/signup/$", ojuser.views.OjUserSignupView.as_view(), name="account_signup"),
    url(r"^account/settings/$", ojuser.views.OjUserSettingsView.as_view(), name="account_settings"),
    url(r"^account/profiles/$", ojuser.views.OjUserProfilesView.as_view(), name="account_profiles"),
    url(r"^account/", include("account.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
