from django.db import models
import uuid


class File(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, db_index=True)
    header = models.CharField(max_length=256, null=True)


class Row(models.Model):
    file = models.ForeignKey('File', related_name='rows', on_delete=models.CASCADE)
    raw_row = models.CharField(max_length=1024)

    def __str__(self):
        return self.raw_row


class Temporal(models.Model):
    file = models.ForeignKey('File', related_name='temporals', on_delete=models.CASCADE)
    row = models.ForeignKey('Row', related_name='temporals', on_delete=models.CASCADE)
    row_index = models.IntegerField()
    column = models.IntegerField()
    startIdx = models.IntegerField()
    endIdx = models.IntegerField()
    text = models.CharField(max_length=256)
    temporal = models.CharField(max_length=256)
    type = models.CharField(max_length=64, default='')
