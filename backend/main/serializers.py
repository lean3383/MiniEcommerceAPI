from .models import Product, Order, OrderDetail
from rest_framework import serializers

class ProductSerial(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price','stock']

    def validate_id(self, value):
        if self.instance and self.instance.id != value:
            raise serializers.ValidationError('This Field can not be edited')
        return value

class OrderDetailSerial(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(many=False, queryset=Product.objects.all())

    class Meta:
        model = OrderDetail
        fields = ['quantity','product']

    def validate(self, data):
        if 'quantity' in data: quantity = data['quantity']
        else: raise serializers.ValidationError({'quantity':
                                f'This field is required'})

        if 'product' in data: product  = data['product']
        else: raise serializers.ValidationError({'product':
                                f'This field is required'})

        if product.stock < quantity:
            raise serializers.ValidationError({'product':
                              f'Product {product.name} without enough stock'})
        return data

class OrderSerial(serializers.ModelSerializer):
    order_details = OrderDetailSerial(many=True)
    total     = serializers.FloatField(source='get_total', read_only= True)
    total_usd = serializers.FloatField(source='get_total_usd', read_only= True)

    class Meta:
        model = Order
        fields = ['id', 'order_details', 'total', 'total_usd', 'date_time']

    def create(self, data):
        details_data = data.pop('order_details')
        order = Order.objects.create(**data)

        for d in details_data:
            OrderDetail.objects.create(order=order, **d)
            d['product'].update_stock(d['quantity'])
        return order

    def update(self, instance, data):
        details_data = data.pop('order_details')
        for d in details_data:
            product  = d.pop('product')
            detail, created = OrderDetail.objects.get_or_create(order=instance,
                                                                product=product,
                                                                defaults=d)
            if created:
                product.update_stock(d['quantity'])
            else:
                OrderDetail.objects.update_or_create(order=instance,
                                                     product=product,
                                                     defaults=d)
                dif = d['quantity'] - detail.quantity
                detail.product.update_stock(dif)
        return instance

    def validate_id(self, value):
        if self.instance and self.instance.id != value:
            raise serializers.ValidationError('This Field can not be edited')
        return value

    def validate(self, data):
        if not 'order_details' in data or not data['order_details']:
            raise serializers.ValidationError({'order_details':
                                f'You need to include at least one order detail'})

        products = [d['product'].id for d in data['order_details']]
        if len(products) != len(set(products)):
            raise serializers.ValidationError({'order_details':
                                f'Just one order_detail per product'})
        return data
