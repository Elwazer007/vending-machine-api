from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Product(models.Model):
    seller = models.ForeignKey(User, verbose_name=_("seller"), on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=120)
    amout_available = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=7, decimal_places=2)
