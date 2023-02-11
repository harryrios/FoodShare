from default import *

def create_account(email: str, password: str, acc_type: str):
    '''
    :param email: an email address
    :type email: str
    :param password: an unencrypted password
    :type password: str
    :param acc_type:
    :type acc_type: str -- "manager" or "shopper
    '''

    if dummy_security_measure(): #TODO: 1. email not registered 2. account type
        # generate a new, unique id
        id=generate_id(table="account")
        # encrypt password
        cypher=encrypt_password(password)
        # make sql query
        sql=f'''
        begin
        insert into account
        values ({id}, {email}, {cypher}, {acc_type})
        commit;
        '''
        # commit sql
        dummy_sql_commit(sql)