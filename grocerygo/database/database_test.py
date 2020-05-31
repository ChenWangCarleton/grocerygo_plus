from grocerygo_plus.grocerygo.database import DatabaseObj

if __name__ == '__main__':
    data=DatabaseObj("localhost","dev","dev",write_access=True)
    #print(''.join(map(str,data.execute_select("show create table test_tb_0"))))
    #print(data.execute_insert('test_tb_0', columnnames=['title','gender','description','phone','statue'],attributes=[('test','1','test_des','874562','1')]))
    """print(data.execute_update('test_tb_0', 'id=1', columnnames=['title','gender','description','phone','statue'],attributes=[('test23','1','test_des','87123212','1')]))
    print(data.select_from_table('test_tb_0'))
    print(data.select_from_table('test_tb_0',where_constraint='statue=1'))
    print(data.execute_insert('test_tb_1', columnnames=['id', 'second_id', 'title'],
                              attributes=[('1', '2', 'test_des')]))
    print(data.select_from_table('test_tb_0 inner join test_tb_1 on test_tb_0.id = test_tb_1.id'))
    print(data.execute_insert('test_tb_1', columnnames=['id', 'second_id', 'title'],
                              attributes=[('11', '2', 'test_des')]))"""
    #print(data.execute_insert('test_tb_0', columnnames=['title','gender','description','phone','statue'],attributes=[('test1','2','test_des','874562','3'),('test2','3','test_des','874562','1')]))
    """
    ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')"""