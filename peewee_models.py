from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, SmallIntegerField
from config import DB_FILE


db = SqliteDatabase(DB_FILE)


class Control(Model):
    filename = CharField(primary_key=True)
    description = CharField(null=True)

    class Meta:
        database = db
        table_name = "control"


class Scandata(Model):
    STATUS_CHOICES = (
        (1, "STATUS_COMPLIANT"),
        (2, "STATUS_NOT_COMPLIANT"),
        (3, "STATUS_NOT_APPLICABLE"),
        (4, "STATUS_ERROR"),
        (5, "STATUS_EXCEPTION"),
    )

    control = ForeignKeyField(Control, related_name="scandata")
    status = SmallIntegerField(choices=STATUS_CHOICES)

    class Meta:
        database = db
        table_name = "scandata"
