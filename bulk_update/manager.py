# coding=utf-8
from __future__ import unicode_literals, print_function

import itertools

from django.db import models, connections

__author__ = 'vadim'


class BulkUpdateQuerySet(models.QuerySet):
    def bulk_update(self, obj_list, update_fields=(), exclude_fields=(), batch_size=100):
        connection = connections[self.db]
        vendor = connection.vendor
        query_builder = None
        pk_field = self.model._meta.pk.name

        update_fields = update_fields or [f.name for f in self.model._meta.fields]
        update_fields = set(update_fields) - set(exclude_fields)

        fields = []
        for field in self.model._meta.fields:
            # attname = field.attname[:-3] if field.attname.endswith('_id') else field.attname
            if isinstance(field, models.AutoField) or field.name not in update_fields:
                continue

            fields.append(field)

        if 'sqlite' in vendor:
            query_builder = self.__sqlite_query

        elif 'mysql' in vendor:
            query_builder = self.__mysql_query

        elif 'postgresql' in vendor:
            query_builder = self.__postgres_query

        assert query_builder, "Vendor '{vendor}' is not support".format(vendor=vendor)

        total_obj_list_count = 0
        for obj_batch in self.__batch_iter(obj_list, batch_size):
            sql, params, obj_list_count = query_builder(self.model._meta, connection, obj_batch, fields, pk_field)

            total_obj_list_count += obj_list_count
            connection.cursor().execute(sql, params)

        return total_obj_list_count

    def __postgres_query(self, meta, connection, obj_list, fields, pk_field):
        """
        UPDATE
            "issue_holiday"
        SET
            "date" = "values"."column2"
        FROM
            (VALUES (1, '2016-01-15'::date), (2, '2016-01-13'::date)) as "values"
        WHERE "issue_holiday"."id" = "values"."column1";
        """
        set_list = []
        for index, field in enumerate(fields):
            set_list.append('"{column}" = "values"."column{index}"'.format(
                column=field.column, index=index+2
            ))

        set_list = ', '.join(set_list)

        params, obj_list_count, values_template = self.__get_values(connection, obj_list, pk_field, fields)

        sql = """
            UPDATE
                "{table}"
            SET
                {set_list}
            FROM
                (VALUES {values_template}) as "values"
            WHERE "{table}"."{pk_field}" = "values"."column1";
        """.format(
            table=meta.db_table,
            set_list=set_list,
            values_template=values_template,
            pk_field=pk_field
        )

        return sql, params, obj_list_count

    def __mysql_query(self, meta, connection, obj_list, fields, pk_field):
        """
        INSERT INTO
            issue_holiday (`id`, `date`)
        VALUES
            (1, '2016-01-22'), (2, '2016-02-14')
        ON DUPLICATE KEY UPDATE
            `date`=VALUES(`date`);
        """
        all_fields = [field for field in meta.fields if not isinstance(field, models.AutoField)]

        insert_list = ['`{}`'.format(pk_field)] + ['`{}`'.format(field.column) for field in all_fields]
        insert = ', '.join(insert_list)

        params, obj_list_count, values_template = self.__get_values(connection, obj_list, pk_field, all_fields)

        update_list = ['`{column}`=VALUES(`{column}`)'.format(column=field.column) for field in fields]
        update = ', '.join(update_list)

        sql = """
            INSERT INTO
                {table} ({insert})
            VALUES
                {values_template}
            ON DUPLICATE KEY UPDATE
                {update};
        """.format(
            table=meta.db_table,
            insert=insert,
            values_template=values_template,
            update=update
        )

        return sql, params, obj_list_count

    def __sqlite_query(self, meta, connection, obj_list, fields, pk_field):
        """
        REPLACE INTO
            issue_holiday ("id", "date")
        VALUES
            (1, '2016-01-22'), (2, '2016-02-14');
        """
        all_fields = [field for field in meta.fields if not isinstance(field, models.AutoField)]
        origin_field = set([field for field in all_fields]) - set([field for field in fields])

        insert_list = ['`{}`'.format(pk_field)] + ['`{}`'.format(field.column) for field in all_fields]
        insert = ', '.join(insert_list)

        if origin_field:
            obj_list = list(obj_list)
            pk_list = [getattr(obj, pk_field) for obj in obj_list]
            origin_obj_map = self.in_bulk(pk_list)

            for obj in obj_list:
                for field in origin_field:
                    value = getattr(origin_obj_map[getattr(obj, pk_field)], field.attname)
                    setattr(obj, field.attname, value)

        params, obj_list_count, values_template = self.__get_values(
            connection, obj_list, pk_field, all_fields)

        sql = """
            REPLACE INTO
                {table} ({insert})
            VALUES
                {values_template}
        """.format(
            table=meta.db_table,
            insert=insert,
            values_template=values_template,
        )

        return sql, params, obj_list_count

    @staticmethod
    def __batch_iter(obj_list, batch_size):
        if batch_size <= 0:
            yield obj_list
            return

        count = len(obj_list)
        steps = count // batch_size + (1 if count % batch_size else 0)

        i = 0
        while i < steps:
            yield itertools.islice(obj_list, i*batch_size, (i+1)*batch_size)
            i += 1

    def __get_values(self, connection, obj_list, pk_field, fields):
        obj_list_count = 0
        params = []

        for obj in obj_list:
            params.append(getattr(obj, pk_field))
            for field in fields:
                params.append(field.get_db_prep_value(getattr(obj, field.attname), connection))

            obj_list_count += 1

        return (
            params,
            obj_list_count,
            ', '.join(['({})'.format(', '.join(['%s'] * (len(fields) + 1)))] * obj_list_count)
        )


class BulkUpdateManager(models.Manager.from_queryset(BulkUpdateQuerySet)):
    pass