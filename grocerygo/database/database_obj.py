import mysql.connector
import logging
import traceback


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class DatabaseObj:
    def __init__(self, hostname, username, password, databasename='grocerygo', write_access=False):
        self.hostname = hostname
        self.username = username
        self.databasename = databasename
        self.write_access = write_access
        try:
            self.mydb = mysql.connector.connect(host=hostname, user=username, password=password,database=databasename)

            logger.debug('class created for host:{} user:{}  to database:{}'.format(hostname,username,
                                                                                               databasename))
        except:
            logger.error('failed to establish connection with database when creating class for host:{} user:{} '
                         'to database:{}\ntraceback:\n{}'.format(hostname,username,databasename,
                                                                          traceback.format_exc()))
    def __del__(self):
        logger.debug('delecting class created for host:{} user:{} to database:{}'.format(self.hostname,
                                                                                                     self.username,
                                                                                                     self.databasename))
        try:
            self.mydb.close()
            logger.debug('connection to database with user:{} closed'.format(self.username))
        except:
            logger.error('error when closing connection to database')


    def execute_insert(self,  table_name, **kwargs):
        # expecting  columnnames (string list), types (string list), attributes (tuple list)in kwargs
        try:
            assert len(kwargs['columnnames']) == len(kwargs['attributes'][0])

            assert len(kwargs['columnnames']) > 0
            for i in kwargs['attributes']:
                assert len(i) == len(kwargs['attributes'][0])
        except:
            logger.error('error when executing insert statement\nkwargs:\n{}\n{}'.format(kwargs,traceback.format_exc()))
            return False
        column_num = len(kwargs['columnnames'])
        sql_statement = 'INSERT INTO {} ({}) VALUES ({})'.format(table_name,
                                                                 ','.join(kwargs['columnnames']),
                                                                 ','.join(['%s' for i in range(column_num)]))
        logger.info(sql_statement)
        #print(sql_statement)

        return self.insert_update(sql_statement,kwargs['attributes'])


    def execute_update(self, table_name, where_constraint, **kwargs):
        # expecting  columnnames (string list), types (string list), attributes (tuple list)in kwargs
        # expecting where_constraint(string) to start with either where or the constraint, not null
        try:
            assert len(kwargs['columnnames']) == len(kwargs['attributes'][0])

            assert len(kwargs['columnnames']) > 0
            for i in kwargs['attributes']:
                assert len(i) == len(kwargs['attributes'][0])

            assert where_constraint
        except:
            logger.error('error when executing update statement\nkwargs:\n{}\n{}'.format(kwargs,traceback.format_exc()))
            return False
        if not where_constraint.lower().startswith('where'):
            where_constraint = 'WHERE ' + where_constraint
        sql_statement = 'UPDATE {} SET {} {}'.format(table_name,
                                                                 ','.join([col_name+'=%s' for col_name in kwargs['columnnames']]),
                                                                 where_constraint)
        logger.info(sql_statement)
        #print(sql_statement)
        return self.insert_update(sql_statement,kwargs['attributes'])

    def insert_update(self, sql_statement, values):
        try:
            cursor = self.mydb.cursor()
            cursor.executemany(sql_statement, values)
            self.mydb.commit()
            row_affected = cursor.rowcount
            #print(row_affected, "was inserted.")
            logger.info('succeeded when executing command:\n{}'.format(sql_statement))
            cursor.close()
            return row_affected
        except:
            logger.debug('Failed when executing command:\n{}\nvalues:{}\n{}'.format(sql_statement,values,traceback.format_exc()))
            return False


    def execute_row_affected(self, sql_statement):
        try:
            cursor = self.mydb.cursor()
            cursor.execute(sql_statement)
            self.mydb.commit()
            row_affected = cursor.rowcount
            #print(row_affected, "was inserted.")
            logger.info('succeeded when executing command:\n{}'.format(sql_statement))
            cursor.close()
            return row_affected
        except:
            logger.debug('Failed when executing command:\n{}\n{}'.format(sql_statement,traceback.format_exc()))
            return False

    def select_from_table(self, table_name, where_constraint='', *column_names):
        if len(column_names) == 0:
            sql_statement = "SELECT * FROM {}".format(table_name)
        else:
            sql_statement = "SELECT {} FROM {}".format(','.join(column_names),table_name)

        if where_constraint:
            if not where_constraint.lower().startswith('where'):
                where_constraint = 'WHERE ' + where_constraint
            sql_statement = sql_statement + ' {}'.format(where_constraint)
        return self.execute_select(sql_statement)


    def execute_delete(self, table_name, where_constraint):
        # expecting where_constraint(string) to start with either where or the constraint, not null
        try:
            assert where_constraint
        except:
            logger.error('error when executing delete statement on table {}\nwith where constraint: {}\n{}'.format(table_name, where_constraint,traceback.format_exc()))
            return False
        if not where_constraint.lower().startswith('where'):
            where_constraint = 'WHERE ' + where_constraint
        sql_statement = 'DELETE FROM {} {}'.format(table_name, where_constraint)
        logger.info(sql_statement)
        return self.execute_row_affected(sql_statement)


    def execute_select(self, sql_statement):
        try:
            cursor = self.mydb.cursor()
            cursor.execute(sql_statement)
            result = cursor.fetchall()
            cursor.close()
            logger.debug('select command:\n{}\nexecuted successfully'.format(sql_statement))
            return result
        except:
            logger.debug('Failed when executing select command:\n{}\n{}'.format(sql_statement,traceback.format_exc()))
            return False