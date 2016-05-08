django-bulk-update
==
Bulk update over Django ORM.

Bulk update given objects using **minmal query** over **Django ORM**.

Support python2.7 and python3.5.

Installation
==
    pip install -e git://github.com/newvadim/django-bulk-update.git#egg=django-bulk-update

    Version 1.0.0
    pip install -e git://github.com/newvadim/django-bulk-update.git@1.0.0#egg=django-bulk-update

Usage
==
    from bulk_update.manager import BulkUpdateManager


    class BulkModel(models.Model):
        ...
        objects = BulkUpdateManager()


    charfields = ['value1', 'value2', 'value3', 'value4']
    obj_list = BulkModel.objects.all()[:4]
    for index, obj in enumerate(obj_list):
        obj.charfield = charfields[index]

    BulkModel.objects.bulk_update(obj_list)  # updates all columns
    BulkModel.objects.bulk_update(obj_list, update_fields=['charfield', 'textfield'])  # updates only name column
    BulkModel.objects.bulk_update(obj_list, exclude_fields=['textfield'])  # updates all columns except textfield

    # Combination update_fields and exclude_fields
    BulkModel.objects.bulk_update(obj_list, update_fields=['charfield', 'textfield'], exclude_fields=['textfield'])

    BulkModel.objects.bulk_update(obj_list, batch_size=1000)  # updates all columns by 1000 sized chunks

Requirements
==
Django 1.2+

License
==
django-bulk-update is released under the MIT License. See the LICENSE file for more details.