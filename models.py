import datetime
import peewee

from config import DB_FILE
from config import STATUS_COMPLIANT, STATUS_NOT_COMPLIANT, STATUS_NOT_APPLICABLE, STATUS_ERROR, STATUS_EXCEPTION

db = peewee.SqliteDatabase(DB_FILE)


class Control(peewee.Model):
    uid = peewee.CharField(null=True)
    filename = peewee.CharField(primary_key=True)
    title = peewee.CharField(null=True)
    requirements = peewee.CharField(null=True)
    description = peewee.CharField(null=True)

    class Meta:
        database = db
        table_name = "control"


class Scandata(peewee.Model):
    STATUS_CHOICES = (
        (STATUS_COMPLIANT, "STATUS_COMPLIANT"),
        (STATUS_NOT_COMPLIANT, "STATUS_NOT_COMPLIANT"),
        (STATUS_NOT_APPLICABLE, "STATUS_NOT_APPLICABLE"),
        (STATUS_ERROR, "STATUS_ERROR"),
        (STATUS_EXCEPTION, "STATUS_EXCEPTION"),
    )

    STATUS_FROM_CODE = dict(STATUS_CHOICES)
    STATUS_CODE = dict(map(reversed, STATUS_CHOICES))

    control = peewee.ForeignKeyField(Control, related_name="scandata")
    status = peewee.SmallIntegerField(choices=STATUS_CHOICES)
    lead_time_sec = peewee.FloatField(default=0)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        table_name = "scandata"
