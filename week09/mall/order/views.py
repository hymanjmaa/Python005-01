from django.contrib.auth.models import User
from .models import Order
from .serializers import OrderSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        # if self.request.method == 'POST':
        serializer.save(buyer_id=self.request.user)


@api_view(['GET'])
def order_cancel(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.is_delete = True
    order.save()
    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication, BasicAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def order_create(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(buyer_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
