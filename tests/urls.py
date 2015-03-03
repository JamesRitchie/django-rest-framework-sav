from django.conf.urls import patterns

from tests.views import MockView

from rest_framework_sav.views import session_auth_view


urlpatterns = patterns(
    '',
    (r'^view/$', MockView.as_view()),
    (r'^auth-session/$', session_auth_view)
)
