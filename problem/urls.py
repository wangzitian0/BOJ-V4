from django.conf.urls import url
from . import views


urlpatterns = [
    #  url(r"^up/$", views.ProblemListView.as_view(), name="problem_list"),
    url(r"^$", views.ProblemListView.as_view(), name="problem-list"),
    url(r'^(?P<pk>[-\w]+)/$', views.ProblemDetailView.as_view(), name='problem-detail'),
]
