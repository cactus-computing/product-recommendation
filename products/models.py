from django.db import models
from store.models import Store

class ProductsModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class ProductAttributes(ProductsModel):
    '''
    Products table. This table contains all of the stores's products and their atributes.
    '''
    product_code = models.IntegerField(unique=False)
    sku = models.CharField(max_length=2000, default=None, null=True, blank=True)
    name = models.CharField(max_length=2000)
    price = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    discounted_price = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    img_url = models.CharField(max_length=2000, default=None)
    permalink = models.CharField(max_length=2000)
    status = models.CharField(max_length=500)
    stock_quantity = models.BooleanField(null=True, blank=True, default=None)
    company = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_created_at = models.DateTimeField()

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __str__(self):
        return self.name

class OrderAttributes(ProductsModel):
    '''
    Order table. This table contains all of the store's orders and their atributes.
    '''
    user = models.CharField(max_length=2000)
    product = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE)
    product_qty = models.IntegerField()
    bill = models.CharField(max_length=2000)
    product_name = models.CharField(max_length=2000)
    company = models.ForeignKey(Store, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            "product_id": self.product_id,
            "bill": self.bill,
            "user": self.user,
            "product_qty": self.product_qty
        }

class CrossSellPredictions(ProductsModel):
    '''
    Cross selling output. A relation of every product and the distance to every other product.
    '''
    product_code = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE)
    recommended_code = models.ForeignKey(
        ProductAttributes, 
        related_name="cross_sell", 
        on_delete=models.CASCADE)
    distance = models.FloatField()
    company = models.ForeignKey(Store, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_code

class UpSellPredictions(ProductsModel):
    '''
    Up selling output. A relation of every product and the distance to every other product.
    '''
    product_code = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE)
    recommended_code = models.ForeignKey(ProductAttributes, related_name="up_sell", on_delete=models.CASCADE)
    distance = models.FloatField()
    company = models.ForeignKey(Store, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_code
