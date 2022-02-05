import pymysql

from configure import *


class DatabaseOperator(object):
    _TAG = "Database: "
    db = pymysql.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        port=DATABASE_PORT,
        charset=DATABASE_CHARSET,
        database=DATABASE_NAME
    )
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

    def close_database(self):
        try:
            self.db.commit()
            self.cursor.close()
            self.db.close()
        except Exception as e:
            logger.error(self._TAG + "Fail to close database, error: " + str(e))

    def insert_one(self, table: str, data: dict, log_tag: str):
        """
        insert one record to database
        :param table: table name
        :param data: data of dict type
        :param log_tag: log's tag
        :return: boolean, true for successful insert
        """
        keys = ','.join(data.keys())
        value = ','.join(['%s'] * len(data))
        sql = f'INSERT INTO {table}({keys}) VALUES ({value});'.format(table=table, keys=keys, value=value)
        try:
            if self.cursor.execute(sql, tuple(data.values())):
                self.db.commit()
                return True
        except Exception as e:
            logger.error(self._TAG + "Fail to insert one record, error: " + str(e) + log_tag)
            self.db.rollback()
            return False

    def insert_many(self, table: str, data_list: list, log_tag: str):
        """
        insert many records to database at once
        :param table: table name
        :param data_list: list of dict type data
        :param log_tag: log's tag
        :return: boolean, true for successful insert
        """
        keys = ','.join(data_list[0].keys())
        value = ','.join(['%s'] * len(data_list[0]))
        sql = f'INSERT INTO {table}({keys}) VALUES ({value});'.format(table=table, keys=keys, value=value)
        try:
            if self.cursor.execute(sql, tuple(tuple(data.values()) for data in data_list)):
                self.db.commit()
                return True
        except Exception as e:
            logger.error(self._TAG + "Fail to insert many records, error: " + str(e) + log_tag)
            self.db.rollback()
            return False

    def select(self, table="", log_tag="", target='*', condition='ture', fetch_one=False, sql=None):
        """
        :param sql: given sql command
        :param table: table name
        :param log_tag: log's tag
        :param target: number or columns of results
        :param condition: screening conditions
        :param fetch_one: return one or many result(s)
        :return: results of sql select
        """
        if sql is None:
            sql = f'SELECT {target} FROM {table} WHERE {condition};'.format(
                target=target, table=table, condition=condition
            )
        try:
            if self.cursor.execute(sql):
                if fetch_one:
                    return self.cursor.fetchone()
                else:
                    return self.cursor.fetchall()
        except Exception as e:
            logger.error(self._TAG + "Fail to select records, error: " + str(e) + log_tag)
            return None

    def update(self, table: str, log_tag: str, column: str, new_value: str, condition: str):
        """
        :param table: table name
        :param log_tag: log's tag
        :param column: the column to be changed
        :param new_value: column's new value
        :param condition: which row to be changed
        :return: boolean of whether succeed to update
        """
        sql = f'UPDATE {table} SET {column}={new_value} WHERE {condition};'.format(
            table=table, column=column, new_value=new_value, condition=condition
        )
        try:
            if self.cursor.execute(sql):
                self.db.commit()
                return True
        except Exception as e:
            logger.error(self._TAG + "Fail to update records, error: " + str(e) + log_tag)
            return False
