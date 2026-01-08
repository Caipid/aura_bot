from __future__ import annotations

from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(primary_key=True)
    university = fields.CharField(default="", max_length=64)
    gtoup = fields.CharField(default="", max_length=64)
