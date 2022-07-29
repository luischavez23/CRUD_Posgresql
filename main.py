import os
import psycopg2
import datetime

DROP_USERS_TABLE = "DROP TABLE IF EXISTS users"
USERS_TABLE = """CREATE TABLE users(
    id SERIAL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
def system_clear(function):
    def wrapper(connect,cursor):
        os.system("cls")
        function(connect,cursor)
        input('')
        os.system("cls")
    wrapper.__doc__ = function.__doc__
    return wrapper

@system_clear
def create_user(connect, cursor):
    """A) Create a new user"""
    username = input('New user: ')
    email = input('email: ')

    query = """INSERT INTO users(username, email) VALUES(%s, %s)"""
    values = (username, email)
    cursor.execute(query, values)
    connect.commit()
    print('\n>>> User created\n')

@system_clear
def show_user(connect, cursor):
    """B) Show users list"""
    query = "SELECT * FROM users"
    cursor.execute(query)
    for id, username, email, created_at in cursor.fetchall():
        print(f'{id} || {username} || {email} || {created_at}')
    connect.commit()

def user_exists(function):
    def wrapper(connect, cursor):
        query = "SELECT id FROM users WHERE id = %s "
        id_number = input('ID number: ')
        cursor.execute(query, (id_number,))
    
        user = cursor.fetchone()
        if user:
            function(id_number, connect, cursor)
        else:
            print('\n>>> Id number doesn\'t exist, type again\n')
    wrapper.__doc__ = function.__doc__
    return wrapper

@system_clear
@user_exists
def delete_user(id_number,connect, cursor):
    """C) Delete an user"""
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (id_number,))
    connect.commit()
    print('\n>>> User deleted\n')

@system_clear
@user_exists    
def update_user(id_number,connect, cursor):
    """D) Update an info"""
    username = input('New name user: ')
    email = input('new email: ')
    created_at = datetime.datetime.now()
    query = "UPDATE users SET username = %s, email = %s, created_at = %s WHERE id = %s"
    values  = (username, email, created_at, id_number)
    cursor.execute(query, values)
    connect.commit()
    print('\n>>> Info updated\n')
    
@system_clear
def default(*args):
    print('\n>>> Invalid option, please type again\n')

if __name__ == '__main__':
    
    options = {
        'a': create_user,
        'b': show_user,
        'c': delete_user,
        'd': update_user
    }

    try:
        connect = psycopg2.connect("postgresql://postgres:admin@localhost/crud_db")

        with connect.cursor() as cursor:
            # cursor.execute(DROP_USERS_TABLE)
            # cursor.execute(USERS_TABLE)
            #connect.commit()
            
            while not False:
                for function in options.values():
                    print(function.__doc__)
                print('To exit, type: \'quit\' or \'q\'')
                
                option = input('Type an option: ').lower()
                
                if option == 'quit' or option == 'q':
                    break
                function = options.get(option, default) 
                function(connect, cursor)
        connect.close()

    except psycopg2.OperationalError as err:
        print('======= Error =======')
        print(err)
    finally:
        print('Connection Succesfully')