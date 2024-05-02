import psycopg2

db_params = {
    'host': 'localhost',
    'database': 'n42',
    'user': 'postgres',
    'password': '1234',
    'port': 5432
}
create_table_person = '''
    create table persons(
        id serial primary key ,
        username varchar(50) not null unique ,
        age int ,
        email varchar(255) not null unique
    );
'''


class DbConnect:
    def __init__(self, db_params):
        self.db_params = db_params

    def __enter__(self):
        self.conn = psycopg2.connect(**self.db_params)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class Person:
    def __init__(self,
                 id: int | None = None,
                 username: str | None = None,
                 age: int | None = None,
                 email: str | None = None):
        self.id = id
        self.username = username
        self.age = age if age > 0 else print('Age must be greater than 0')
        self.email = email

    @staticmethod
    def get_user():
        username = str(input('Enter your username: '))
        with DbConnect(db_params) as conn:
            with conn.cursor() as cur:
                select_user_query = 'select * from persons where username=%s'
                cur.execute(select_user_query, (username,))
                data = cur.fetchone()
                if data:
                    user = Person(id=data[0], username=data[1], age=data[2], email=data[3])
                    return user
                else:
                    raise Exception('User not found')



    def __repr__(self):
        return f'{self.username} - {self.id}'


#
#
# with DbConnect(db_params) as conn:
#     with conn.cursor() as cur:
#         cur.execute(create_table_person)

print(Person.get_user())
