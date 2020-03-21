from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from sendit.apps.core.helpers.enum import Status
from sendit.apps.core.improvised_permissions import user_or_admin
from sendit.apps.core.pagination import StandardPagination
from sendit.apps.core.permissions import IsAdminOnly, IsOwnerOrAdmin

from .models import ParcelDelivery
from .renderers import ParcelDeliveryJsonRenderer
from .serializers import ParcelDeliverySerializer
from .utils import get_parcel, parcel_not_found


class ListCreateParcelDelivery(ListCreateAPIView):
    queryset = ParcelDelivery.objects.filter(is_deleted=False)
    serializer_class = ParcelDeliverySerializer
    renderer_classes = (ParcelDeliveryJsonRenderer,)
    permission_classes = (
        IsAuthenticated,
        IsAdminOnly,
    )

    def get(self, request):
        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(self.queryset, request)
        serializer = ParcelDeliverySerializer(
            result_page, context={"request": request}, many=True
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        parcel = request.data.get("parcel", {})
        serializer = self.serializer_class(data=parcel, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateParcelDelivery(RetrieveUpdateDestroyAPIView):
    """
    This class retrieves, updates, and deletes a single parcel
    """

    queryset = ParcelDelivery.objects.filter(is_deleted=False)
    serializer_class = ParcelDeliverySerializer
    renderer_classes = (ParcelDeliveryJsonRenderer,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get(self, request, id):
        """
        This method retrieves a parcel
        """
        user_or_admin(request.user, get_parcel(id))
        return super().get(request, id)

    def update(self, request, id):
        """
        This method updates a parcel
        """

        parcel = get_parcel(id)
        user_or_admin(request.user, parcel)
        parcel_data = request.data.get("parcel", {})
        serializer = self.serializer_class(
            parcel, data=parcel_data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Overide the default django error message after deleting a parcel
        """
        parcel = get_parcel(id)
        user_or_admin(request.user, parcel)
        parcel.is_deleted = True
        parcel.save()
        return Response({"message": "Parcel Deleted Successfully"})


class UserParcels(ListAPIView):

    serializer_class = ParcelDeliverySerializer
    renderer_classes = (ParcelDeliveryJsonRenderer,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "user_id"

    def get(self, request, user_id):
        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(
            ParcelDelivery.objects.filter(user=user_id), request
        )
        serializer = ParcelDeliverySerializer(
            result_page, context={"request": request}, many=True
        )
        return paginator.get_paginated_response(serializer.data)
