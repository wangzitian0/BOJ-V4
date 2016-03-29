from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^$", views.ProblemListView.as_view(), name="problem-list"),
    url(r'^add/$', views.ProblemCreateView.as_view(), name='problem-add'),
    url(r'^(?P<pk>[0-9]+)/$', views.ProblemDetailView.as_view(), name='problem-detail'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.ProblemUpdateView.as_view(), name='problem-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.ProblemDeleteView.as_view(), name='problem-delete'),
]
