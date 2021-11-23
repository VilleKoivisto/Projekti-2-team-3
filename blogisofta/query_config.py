""" Init parser """

from get_login import login_data

def config():
    """ Palauta tietokannan yhteystiedot """
    
    # käyttäjänimi ja passu haetaan Secret Managerista
    user_name, passwd = login_data()

    # host täytyy muuttaa vastaamaan postgresin ip:tä kubessa:
    db = {'host': '127.0.0.1', 'database': 'blogi', 'port': '5432', 'user': user_name, 'password': passwd}
    
    return db