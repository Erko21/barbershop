from tortoise.fields.base import CASCADE
from tortoise.models import Model
from tortoise import fields

from app.models.propositions import Proposition
from app.models.user import User


class Record(Model):
    id = fields.IntField(pk=True)
    customer_email = fields.CharField(null=False, max_length=128)
    proposition: fields.ForeignKeyRelation[Proposition] = fields.ForeignKeyField(
        "models.Proposition",
        related_name="records",
        on_delete=fields.CASCADE,
        null=False,
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="records", on_delete=fields.CASCADE, null=False
    )
    time = fields.DatetimeField(null=False)

    class Meta:
        table = "records"
