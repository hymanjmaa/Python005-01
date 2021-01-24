from django.db import models
# Create your models here.


class Order(models.Model):
    DELETE_SELECT = (
        (False, "Normal"),
        (True, "Cancel")
    )

    order_id = models.IntegerField(primary_key=True, auto_created=True)
    product_id = models.IntegerField()
    buyer_id = models.ForeignKey(
        'auth.User', related_name='orders', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, choices=DELETE_SELECT)

    class Meta:
        ordering = ['create_time']

    def __str__(self):
        return self.product_id
