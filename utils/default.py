import hashlib
import datetime

from random import random

def dummy_security_measure() -> bool:
    '''
    To replace with actual security...
    '''

    cond = True
    return cond

def dummy_sql_commit(sql: str) -> ...: #TODO: typing, look into Postgres Hook
    '''
    Replace with sql hook

    Return true or false depending on return,
        if return is empty, return false
    '''

    cond = True
    return cond

# returns an encrypted password
def encrypt_password(password: str) -> str:
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()

# returns a new, unique id for any given table
def generate_id(table: str) -> int:
    flag=True
    while flag:
        rand_id=random.randint(0, 9999999)
        sql=f'''
        select id
        from {table}
        where id={rand_id};
        '''
        flag=dummy_sql_commit(sql)
    return rand_id
