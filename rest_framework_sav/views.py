"""Views for Django Rest Framework Session Endpoint extension."""

from django.contrib.auth import login, logout

from rest_framework import parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class SessionAuthView(APIView):

    """Provides methods for REST-like session authentication."""

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser
    )
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        """Login using posted username and password."""
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'detail': 'Session login successful.'})

    def delete(self, request):
        """Logout the current session."""
        logout(request)
        return Response({'detail': 'Session logout successful.'})


session_auth_view = SessionAuthView.as_view()
