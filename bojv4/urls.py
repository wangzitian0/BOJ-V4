from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin

from rest_framework import routers
from problem.views import ProblemViewSet, ProblemDataViewSet
from problem.views import SubmissionViewSet, LanguageViewSet, FileViewSet
from ojuser.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'files', FileViewSet)
router.register(r'problems', ProblemViewSet)
router.register(r'problemdatas', ProblemDataViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("ojuser.urls")),
    url(r"^problem/", include("problem.urls", namespace="problem")),
    url(r"^api/", include(router.urls)),
    url(r"^api-auth/", include('rest_framework.urls', namespace="rest_framework")),
    url(r"^filer/", include("filer.urls")),
    url(r'^', include('filer.server.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
