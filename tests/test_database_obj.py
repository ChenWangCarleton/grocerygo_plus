import time
import datetime
import pytest
import logging

LOGGER = logging.getLogger(__name__)
from grocerygo_plus.grocerygo.database import DatabaseObj


class Testdatabase_obj:

    def setup_class(self):
        self.data = DatabaseObj("localhost", "dev", "dev", write_access=True)
    def test_execute_insert(self):
        
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        id = str(int(ts/86400)%365) + str(int(ts)%86400)
        assert self.data.execute_insert('test_tb_2', columnnames=['id','time','time_null','description','description_null'],attributes=[(id,timestamp,None,'test_execute_insert',None)]) == 1


    def test_execute_update(self):
        
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        id = str(int(ts) % 86400) + str(int(ts / 86400 )% 365)
        print(id)
        self.data.execute_insert('test_tb_2',
                        columnnames=['id', 'time', 'time_null', 'description', 'description_null'],
                        attributes=[(id, timestamp, None, str(ts), None)])
        self.data.execute_update('test_tb_2', 'id = {}'.format(id),
                        columnnames=['description_null'],
                        attributes=[(str(ts),)])
        print('here')
        print(id)
        print(self.data.select_from_table('test_tb_2','id = {}'.format(id), 'description_null'))
        assert self.data.select_from_table('test_tb_2','id = {}'.format(id), 'description_null')[0][0] == ts

    def test_insert_update(self):
        
        assert self.data.insert_update('INSERT INTO test_tb_0 (title, gender, description, phone, statue) VALUES (%s,%s,%s,%s,%s)',[('test23', '1', 'test_insert_update', '87123212', '1')]) == 1



    def test_execute_row_affected(self):
        
        assert self.data.execute_row_affected("INSERT INTO test_tb_0 (title, gender, description, phone, statue) VALUES ('test23','1','test_execute_row_affected','87123212','1')") == 1


    def test_select_from_table(self):
        
        self.data.execute_insert('test_tb_0', columnnames=['title','gender','description','phone','statue'],attributes=[('test','1','test_select_from_table','874562','1')])
        assert len(self.data.select_from_table('test_tb_0', where_constraint="description='test_select_from_table'"))>0

    def test_execute_delete(self):
        
        self.data.execute_insert('test_tb_0', columnnames=['title','gender','description','phone','statue'],attributes=[('test','1','test_execute_delete','874562','1')])
        assert self.data.execute_delete('test_tb_0', "description='test_execute_delete'") > 0

    def test_execute_select(self):
        
        ts = time.time()
        id = str(int(ts/86400)%365) + str(int(ts)%86400)
        description = str(int(ts)%86400) + str(int(ts/86400)%365)
        self.data.execute_insert('test_tb_0', columnnames=['title','gender','description','phone','statue'],attributes=[('test','1','test_execute_select','874562','1')])
        self.data.execute_update('test_tb_0', 'id = 1',
                     columnnames=['description'],
                     attributes=[(description,)])
        self.data.execute_insert('test_tb_1', columnnames=['id','second_id','title'],attributes=[('1',id,'test_execute_select')])
        result = self.data.execute_select('SELECT test_tb_0.description, test_tb_1.second_id, test_tb_1.title FROM test_tb_0 INNER JOIN test_tb_1 ON test_tb_0.id = test_tb_1.id')
        flag = False
        for record in result:
            if str(record[0]) == description and str(record[1]) == id and record[2] == 'test_execute_select':
                # beware of the auto type conversion https://dev.mysql.com/doc/refman/5.7/en/type-conversion.html
                # https://stackoverflow.com/questions/21762075/mysql-automatically-cast-convert-a-string-to-a-number
                # (description, id, 'test_execute_select')
                flag = True
        assert flag

