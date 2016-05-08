# coding=utf-8
from __future__ import unicode_literals, print_function

import random

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from test_site.test_app.models import BulkModel, BulkRelatedModel

__author__ = 'vadim'


class BulkUpdateTests(TestCase):
    multi_db = True
    db_list = [
        'sqlite',
        'mysql',
        'postgres',
    ]

    def setUp(self):
        self.data = {db: {} for db in self.db_list}
        self.data_all_fields = set([f.name for f in BulkModel._meta.fields[1:]])
        self.data_all_fields_len = len(self.data_all_fields)

        for db in self.db_list:
            self.data[db]['foreignkey_before'] = BulkRelatedModel.objects.using(db).create()
            self.data[db]['foreignkey_after'] = BulkRelatedModel.objects.using(db).create()

            self.data[db]['now'] = timezone.now()
            self.data[db]['timefield_before'] = self.data[db]['now'].time()
            self.data[db]['timefield_after'] = (self.data[db]['now'] + timedelta(minutes=1)).time()

            self.data[db]['datefield_before'] = timezone.now().date()
            self.data[db]['datefield_after'] = self.data[db]['datefield_before'] + timedelta(days=1)

            self.data[db]['datetimefield_before'] = timezone.now()
            self.data[db]['datetimefield_after'] = self.data[db]['datetimefield_before'] + timedelta(minutes=1)

            self.data[db]['bulkmodel_before'] = BulkModel(
                foreignkey=self.data[db]['foreignkey_before'],
                charfield='before',
                emailfield='before@mail.mail',
                slugfield='before',
                urlfield='http://before.before',
                commaseparatedintegerfield='1,2,3',
                textfield='before',
                smallintegerfield=101,
                positivesmallintegerfield=102,
                integerfield=103,
                positiveintegerfield=104,
                bigintegerfield=105,
                floatfield=106.0,
                timefield=self.data[db]['timefield_before'],
                datefield=self.data[db]['datefield_before'],
                datetimefield=self.data[db]['datetimefield_before'],
                booleanfield=False,
                nullbooleanfield=None,
                genericipaddressfield='127.0.0.1',
                filepathfield='/filepathfield_before.txt',
                filefield='/filefield_before.txt',
                imagefield='/imagefield_before.txt',
            )

            BulkModel.objects.using(db).bulk_create([self.data[db]['bulkmodel_before']]*100)

            self.data[db]['bulkmodel_after'] = BulkModel(
                foreignkey=self.data[db]['foreignkey_after'],
                charfield='after',
                emailfield='after@mail.mail',
                slugfield='after',
                urlfield='http://after.after',
                commaseparatedintegerfield='1,2,3',
                textfield='after',
                smallintegerfield=201,
                positivesmallintegerfield=202,
                integerfield=203,
                positiveintegerfield=204,
                bigintegerfield=205,
                floatfield=206.0,
                timefield=self.data[db]['timefield_after'],
                datefield=self.data[db]['datefield_after'],
                datetimefield=self.data[db]['datetimefield_after'],
                booleanfield=True,
                nullbooleanfield=False,
                genericipaddressfield='127.0.0.2',
                filepathfield='/filepathfield_after.txt',
                filefield='/filefield_after.txt',
                imagefield='/imagefield_after.txt',
            )

    def _check_after_fields(self, db, obj, check_fields):
        for field in check_fields:
            after_value = getattr(self.data[db]['bulkmodel_after'], field)
            obj_value = getattr(obj, field)
            self.assertEqual(after_value, obj_value)

    def _check_before_fields(self, db, obj, check_fields):
        for field in check_fields:
            before_value = getattr(self.data[db]['bulkmodel_before'], field)
            obj_value = getattr(obj, field)
            self.assertEqual(before_value, obj_value, 'Field {} was changed.'.format(field))

    def _check_obj_list(self, check_fields, update_fields=(), exclude_fields=()):
        for db in self.db_list:
            obj_list = BulkModel.objects.using(db).order_by('id')[1:]
            for obj in obj_list:
                for field in check_fields:
                    after_value = getattr(self.data[db]['bulkmodel_after'], field)
                    setattr(obj, field, after_value)

            BulkModel.objects.using(db).bulk_update(
                obj_list, update_fields=update_fields, exclude_fields=exclude_fields)

            obj_list = BulkModel.objects.using(db).order_by('id')[1:]
            for obj in obj_list:
                self._check_after_fields(db, obj, check_fields)

                check_before_fields = self.data_all_fields - check_fields
                self._check_before_fields(db, obj, check_before_fields)

            first = BulkModel.objects.using(db).order_by('id').first()
            self._check_before_fields(db, first, check_fields)

    def test_all_fields(self):
        self._check_obj_list(check_fields=self.data_all_fields)

    def test_update_fields(self):
        update_fields = {
            'bigintegerfield',
            'booleanfield',
            'commaseparatedintegerfield',
            'datetimefield',
            'emailfield',
            'floatfield',
            'foreignkey',
            'integerfield',
            'positiveintegerfield',
            'textfield',
            'timefield',
        }
        self._check_obj_list(check_fields=update_fields, update_fields=update_fields)

    def test_exclude_fields(self):
        exclude_fields = {
            'charfield',
            'commaseparatedintegerfield',
            'datefield',
            'emailfield',
            'filefield',
            'imagefield',
            'integerfield',
            'nullbooleanfield',
            'positivesmallintegerfield',
            'slugfield',
            'textfield'
        }
        check_fields = self.data_all_fields - exclude_fields
        self._check_obj_list(check_fields=check_fields, exclude_fields=exclude_fields)

    def test_combo(self):
        update_fields = {
            'bigintegerfield',
            'booleanfield',
            'commaseparatedintegerfield',
            'datetimefield',
            'emailfield',
            'floatfield',
            'foreignkey',
            'integerfield',
            'positiveintegerfield',
            'textfield',
            'timefield',
        }

        exclude_fields = {
            'charfield',
            'commaseparatedintegerfield',
            'datefield',
            'emailfield',
            'filefield',
            'imagefield',
            'integerfield',
            'nullbooleanfield',
            'positivesmallintegerfield',
            'slugfield',
            'textfield'
        }

        check_fields = {
            'bigintegerfield',
            'booleanfield',
            'datetimefield',
            'floatfield',
            'foreignkey',
            'positiveintegerfield',
            'timefield'
        }

        self._check_obj_list(check_fields=check_fields, update_fields=update_fields, exclude_fields=exclude_fields)

    def test_combo_random_fields(self):
        all_fields = list(self.data_all_fields)
        update_fields = {random.choice(all_fields) for i in range(10)}
        exclude_fields = {random.choice(all_fields) for i in range(10)}
        check_fields = update_fields - exclude_fields

        self._check_obj_list(check_fields=check_fields, update_fields=update_fields, exclude_fields=exclude_fields)
