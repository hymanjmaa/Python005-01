from django.contrib import admin
from .models import Order
# Register your models here.

admin.site.register(Order)

from django.contrib.auth import get_user_model
User = get_user_model()
