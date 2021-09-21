from fastapi.datastructures import Default
from tortoise.models import Model
from tortoise import fields
from enum import Enum


class Role(str, Enum):
    ADMiN = "Admin"
    BARBER = "Barber"
    CUSTOMER = "Customer"


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32, unique=True, null=False)
    hash_password = fields.CharField(max_length=128)
    full_name = fields.CharField(null=False, max_length=128)
    email = fields.CharField(null=False, max_length=255, unique=True)
    role = fields.CharEnumField(enum_type=Role)
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)

    class Meta:
        table = "users"
