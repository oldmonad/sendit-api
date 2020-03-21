from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from sendit.apps.core.api_exceptions import ResourceDoesNotExist
from sendit.apps.core.pagination import StandardPagination

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ListProfile(ListAPIView):
    renderer_classes = (ProfileJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        paginator = StandardPagination()
        queryset = Profile.objects.all().exclude(user=self.request.user)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProfileRetrieveAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def get(self, request, email, *args, **kwargs):
        try:
            profile = Profile.objects.select_related("user").get(user__email=email)
        except Profile.DoesNotExist:
            raise ResourceDoesNotExist

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, email):

        if request.user.email != email:
            error_message = {
                "error": "You are not allowed to update the details for user {}".format(
                    email
                )
            }
            return Response(error_message, status=status.HTTP_403_FORBIDDEN)
        user_data = request.data.get("profile", {})

        serializer = ProfileSerializer(
            request.user.profile,
            data=user_data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            self.check_object_permissions(request, user_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
