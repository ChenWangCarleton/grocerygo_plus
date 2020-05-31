from grocerygo_plus.database import DatabaseObj

if __name__ == '__main__':
    data=DatabaseObj("localhost","dev","dev",write_access=True)



    #print(data.execute_insert('test_tb_0', columnnames=['title','gender','description','phone','statue'],attributes=[('test','1','test_des','874562','1')]))

    #print(data.execute_insert('test_tb_0', columnnames=['title','gender','description','phone','statue'],attributes=[('test1','2','test_des','874562','3'),('test2','3','test_des','874562','1')]))

