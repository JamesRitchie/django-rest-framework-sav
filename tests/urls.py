from django.conf.urls import patterns

from tests.views import MockView


urlpatterns = patterns(
    '',
    (r'^view/$', MockView.as_view()),
    (r'^auth-session/$', 'rest_framework_se.views.session_auth_view')
)
