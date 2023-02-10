from setup_db import create_tables ,create_fake_data,execute_query


#pytest example
def test_db():
    create_tables()
    create_fake_data(students_num=20)
    num=int(execute_query("SELECT COUNT(student_id) FROM students")[0][0])
    assert num==20

def test_tachers_db():
    create_tables()
    create_fake_data(teachers_num=10)
    num=int(execute_query("SELECT COUNT(teacher_id) FROM teachers")[0][0])
    assert num==16