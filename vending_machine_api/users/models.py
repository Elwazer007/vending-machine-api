from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from model_utils.choices import Choices

ROLES = Choices(
    ("buyer", _("Buyer")),
    ("seller", _("Seller")),
)


class User(AbstractUser):
    role = models.CharField(
        _("role"),
        max_length=30,
        choices=ROLES,
        default=ROLES.buyer,
    )

    deposit = models.PositiveIntegerField(
        default=0
    )


# Create your models here.
