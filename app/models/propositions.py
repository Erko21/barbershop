from tortoise.models import Model
from tortoise import fields


class Proposition(Model):
    id = fields.IntField(pk=True)
    proposition_name = fields.CharField(null=False, max_length=128)
    price = fields.DecimalField(max_digits=6, decimal_places=2)
    job_time = fields.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        table = "propostitons"
