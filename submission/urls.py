from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^$", views.SubmissionListView.as_view(), name="submission-list"),
    url(r'^add/(?P<pid>[0-9]+)/$', views.SubmissionCreateView.as_view(), name='submission-add'),
    url(r'^(?P<pk>[0-9]+)/$', views.SubmissionDetailView.as_view(), name='submission-detail'),
]
