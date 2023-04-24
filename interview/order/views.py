from django.shortcuts import render
from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer
from rest_framework import generics, status
from rest_framework.response import Response


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(generics.UpdateAPIView):
    """
    A generic update view that sets the is_active state on an order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # set is_active state of an order to False.
        order.is_active = False
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
