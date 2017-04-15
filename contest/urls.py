from django.conf.urls import url
from . import views


urlpatterns = [
        url(r'^$', views.listContestByUser, name='contest-list'),
        url(r'^(?P<cid>\d+)/$', views.showContest, name='show_contest'),
        url(r'^(?P<cid>\d+)/board$', views.showBoard, name='show_board'),
        url(r'^(?P<cid>\d+)/status', views.showStatus, name='show_status'),
         url(r'^(?P<cid>\d+)/query', views.showQuery, name='show_query'),
        url(r'^(?P<cid>\d+)/problem/(?P<cpidx>[A-Z])/$', views.showContestProblem, name="contest_problem"),

        url(r'^testproblem/$', views.testProblem, name="testproblem"),

        #url(r'^contestself$', views.listContestByUserSelf),
        ]