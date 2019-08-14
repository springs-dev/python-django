from rest_framework import mixins, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Stuff
from .serializers import FeedbackSerializer, StuffSerializer


class StuffViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
    View for CRUD operations Stuff
    """

    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Stuff.objects.all()
    serializer_class = StuffSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        query = super(StuffViewSet, self).get_queryset()
        if self.request.user.is_staff:
            return query
        return query.filter(account=self.request.user).all()

    @action(methods=['post'], url_path='feedback', detail=True, url_name='feedback')
    def set_feedback(self, request, pk):
        stuff = self.get_object()
        serializer = FeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(voucher=stuff, account=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
