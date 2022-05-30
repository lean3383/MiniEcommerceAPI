from django.db         import models
from django.core.cache import cache
from django.core.validators import MinValueValidator
import requests

class Product(models.Model):
    id    = models.CharField(max_length=10, primary_key=True)
    name  = models.CharField(max_length=30)
    price = models.FloatField(validators=[MinValueValidator(0.01)])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def update_stock(self, quantity):
        self.stock -= quantity
        self.save()

class Order(models.Model):
    id         = models.CharField(max_length=10, primary_key=True)
    date_time  = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        query = OrderDetail.objects.filter(order=self)
        return sum([q.quantity * q.product.price
                 if q.product is not None else 0 for q in query])

    def get_total_usd(self):
        if cache.get('usd'):
            usd= cache.get('usd')

        else:
            url = f'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
            usd = requests.get(url).json()
            usd = [d['casa']['venta'] for d in usd
                    if d.get('casa').get('nombre') == 'Dolar Blue'][0]
            cache.set('usd', usd)

        tot = self.get_total() / float(usd.replace(',','.'))
        tot = round(tot, 2)
        return tot

class OrderDetail(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE,
                                 related_name='order_details')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['order', 'product']
