from utils.default import *
from utils.postgres_utils import *
from datetime import datetime
from sqlalchemy.engine import Engine

def create_transaction(shopper_id: int, pantry_id: int, item_id: int,
                       action: str, quantity: int, description: str,
                       engine: Engine): #TODO: add typing/output
    '''
    :param shopper_id: the id of the requesting shopper
    :param pantry_id: the id of the pantry to which the request is made
    :param item_id: the id of the item within said pantry's inventory
    :param action: the type of request
    :type action: 'request' or 'donate'
    :param quantity: the quantity of item_id to be added or subtracted to the inventory
    :param description: a user-generated description of the request to be transmitted to the pantry's manager
    :type description: str of length <= 400
    '''

    #TODO: DOES NOT WORK WITH DONATE -- how to get item_id if item isn't in the pantry's inventory already??

    if dummy_security_measure():
        '''
        Security:
        
        1. check shopper_id, pantry_id, item_id exists
        2. request action is 'donate' or 'receive'
        3. request quantity <= item quantity
        4. description length <= 400
        '''
        # generate a new, unique id
        id = generate_id(table="transaciton")
        # make request_time
        curr_dt = datetime.now()
        # make sql query
        sql=f'''
        begin
        insert into transaciton
        values ({id},{shopper_id},{pantry_id},{item_id},{curr_dt},'pending',{action},{quantity},'{description}')
        commit;
        '''

        # commit sql
        exec_sql(engine, sql)

        # TODO: add trigger to notify pantry manager?
        return...
    return ...

def update_transaction(transaction_id: id, new_status: str):  # TODO: add typing/output
    '''
    :param transaction_id: the id of the transaction to be updated
    :param new_status: the updated transaction status, specified by the manager
    :type new_status: 'approved' or 'denied'
    '''

    if dummy_security_measure():
        '''
        Security:
        
        1. transaction_id exists
        2. new status is 'approved' or 'denied'
        3. function is called by managers on transactions with their pantries
        '''

        sql=f'''
        begin
        update transaction
        set request_status='{new_status}'
        where id={transaction_id}
        commit;
        '''

        # commit sql
        exec_sql(engine, sql)

        # TODO: add trigger to notify shopper?
        return ...
    return ...