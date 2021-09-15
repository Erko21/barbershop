from tortoise import fields
from tortoise.models import Model
from enum import Enum, IntEnum


class Role(str, Enum):
    ADM = "Admin"
    BARB = "Barber"
    CUS = "Customer"


class User(Model):
    class Meta:
        table = "users"

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32)
    hash_password = fields.CharField(max_length=128)
    email = fields.CharField(null=False, max_length=255)
    role = fields.CharEnumField(Role)
    is_active = fields.BooleanField(null=False, default=False)
    full_name = fields.CharField(null=False, max_length=128)
    is_superuser = fields.BooleanField(null=False, default=False)
