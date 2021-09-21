from app.models.propositions import Proposition
from tortoise.fields.base import CASCADE
from app.models.user import User
from tortoise.models import Model
from tortoise import fields


class Record(Model):
    id = fields.IntField(pk=True)
    customer_email = fields.CharField(null=False, max_length=128)
    proposition: fields.ForeignKeyRelation[Proposition] = fields.ForeignKeyField(
        "models.Proposition",
        related_name="propositions",
        on_delete=fields.CASCADE,
        null=True,
    )
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="records", on_delete=fields.CASCADE, null=True
    )
    time = fields.DatetimeField(auto_now=False, auto_now_add=False)

    class Meta:
        table = "records"
