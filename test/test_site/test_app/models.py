# coding=utf-8
from __future__ import unicode_literals

from django.db import models

from bulk_update.manager import BulkUpdateManager

__author__ = 'vadim'


class BulkRelatedModel(models.Model):
    pass


class BulkModel(models.Model):
    foreignkey = models.ForeignKey(to=BulkRelatedModel, related_name='foreignkey')
    charfield = models.CharField(max_length=255)
    emailfield = models.EmailField()
    slugfield = models.SlugField()
    urlfield = models.URLField()
    commaseparatedintegerfield = models.CommaSeparatedIntegerField(max_length=255)
    textfield = models.TextField()
    smallintegerfield = models.SmallIntegerField()
    positivesmallintegerfield = models.PositiveSmallIntegerField()
    integerfield = models.IntegerField()
    positiveintegerfield = models.PositiveIntegerField()
    bigintegerfield = models.BigIntegerField()
    floatfield = models.FloatField()
    timefield = models.TimeField()
    datefield = models.DateField()
    datetimefield = models.DateTimeField()
    booleanfield = models.BooleanField()
    nullbooleanfield = models.NullBooleanField()
    genericipaddressfield = models.GenericIPAddressField()
    filepathfield = models.FilePathField()
    filefield = models.FileField()
    imagefield = models.ImageField()

    objects = BulkUpdateManager()
