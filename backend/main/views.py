from rest_framework             import viewsets
from rest_framework.permissions import IsAuthenticated
from .models      import Product, Order, OrderDetail
from .serializers import ProductSerial, OrderSerial

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset         = Product.objects.all()
    serializer_class = ProductSerial

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset         = Order.objects.all()
    serializer_class = OrderSerial

    def destroy(self, request, pk=None):
        details = OrderDetail.objects.filter(order=self.get_object())
        for d in details:
            if d.product is not None: d.product.update_stock(-d.quantity)
        return super().destroy(request, pk)
