from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework      import status
from .models import Product, Order, OrderDetail

class JWTtest(APITestCase):
    def test_jwt_login_ok(self):
        User.objects.create_user(username='test',
                                 email='test@mail.com',
                                 password='test')
        resp = self.client.post('/api/token/', {'username':'test', 'password':'test'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)

    def test_jwt_login_not(self):
        resp = self.client.post('/api/token/', {'username':'test', 'password':'test'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_without_credentials(self):
        resp = self.client.get('/product/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

class APPtest(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test',
                                 email='test@mail.com',
                                 password='test')
        resp = self.client.post('/api/token/', {'username':'test', 'password':'test'})
        token = resp.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        p1 = {'id':'PK1', 'name':'Producto 1', 'price': 105.4, 'stock': 100}
        p1 = Product.objects.create(**p1)
        p2 = {'id':'PK2', 'name':'Producto 2', 'price': 5334, 'stock': 10}
        p2 = Product.objects.create(**p2)

        o1 = Order.objects.create(id='ORD1')
        d1 = {'order':o1, 'product':p1, 'quantity':5}
        OrderDetail.objects.create(**d1)
        d2 = {'order':o1, 'product':p2, 'quantity':10}
        OrderDetail.objects.create(**d2)
        o2 = Order.objects.create(id='ORD2')
        d3 = {'order':o2, 'product':p1, 'quantity':35}
        OrderDetail.objects.create(**d3)

    def test_create_product(self):
        p = {  'id':'PK3',
              'name':'Producto 3',
             'price': 3223,
             'stock': 100
             }
        count = Product.objects.all().count()

        resp = self.client.post('/product/',p, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), count + 1)

    def test_price_zero(self):
        p = {  'id':'PK4',
              'name':'Producto 4',
             'price': 0,
             'stock': 100
             }
        count = Product.objects.all().count()

        resp = self.client.post('/product/',p, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.all().count(), count)

    def test_create_without_stock(self):
        p = {  'id':'PK4',
              'name':'Producto 4',
             'price': 345
             }
        count = Product.objects.all().count()

        resp = self.client.post('/product/',p, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.all().count(), count + 1)

    def test_list_product(self):
        count = Product.objects.all().count()

        resp = self.client.get('/product/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), count)

    def test_get_product(self):

        resp = self.client.get('/product/PK2/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['id'], 'PK2')

    def test_update_stock(self):
        newStock = 15
        p = { 'stock':newStock }

        resp = self.client.post('/product/PK2/',p, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(id='PK2').stock, newStock)

    def test_update_id(self):
        p = { 'id':'PKKK3' }

        resp = self.client.post('/product/PK2/',p, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        count = Product.objects.all().count()

        resp = self.client.delete('/product/PK2/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), count - 1)

    def test_list_order(self):
        count = Order.objects.all().count()

        resp = self.client.get('/order/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), count)

    def test_get_order(self):

        resp = self.client.get('/order/ORD1/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['id'], 'ORD1')

    def test_create_order(self):
        o = {          'id': 'ORD3',
             'order_details':[{ 'product':'PK1', 'quantity':33 }]
             }
        count = Order.objects.all().count()
        stock = Product.objects.get(id='PK1').stock

        resp = self.client.post('/order/',o, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.all().count(), count + 1)
        #Update Stock
        newStock = Product.objects.get(id='PK1').stock
        self.assertEqual(newStock, stock - 33)

    def test_without_details(self):
        o = {           'id': 'ORD3',
             'order_details':[]
             }
        count = Order.objects.all().count()

        resp = self.client.post('/order/',o, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.all().count(), count)

    def test_create_quantity_zero(self):
        o = {           'id': 'ORD3',
             'order_details':[{ 'product':'PK1', 'quantity':0 }]
             }
        count = Order.objects.all().count()

        resp = self.client.post('/order/',o, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.all().count(), count)

    def test_exceeds_stock(self):
        o = {           'id': 'ORD3',
             'order_details':[{ 'product':'PK2', 'quantity':11 }]
             }
        count = Order.objects.all().count()

        resp = self.client.post('/order/',o, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.all().count(), count)

    def test_update_order(self):
        o = {'order_details':[{ 'product':'PK1', 'quantity':10 }]}
        stock = Product.objects.get(id='PK1').stock
        oldQuantity = OrderDetail.objects.get(order='ORD1', product='PK1').quantity

        resp = self.client.post('/order/ORD1/',o, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        #Update Stock
        newStock = Product.objects.get(id='PK1').stock
        self.assertEqual(newStock, stock + oldQuantity - 10)

    def test_delete_order(self):
        count = Order.objects.all().count()
        stock = Product.objects.get(id='PK1').stock
        oldQuantity = OrderDetail.objects.get(order='ORD2', product='PK1').quantity

        resp = self.client.delete('/order/ORD2/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.all().count(), count - 1)
        #Update Stock
        newStock = Product.objects.get(id='PK1').stock
        self.assertEqual(newStock, stock + oldQuantity)
