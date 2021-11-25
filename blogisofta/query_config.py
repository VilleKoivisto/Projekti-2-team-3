""" Init parser """

from get_login import login_data

def config():
    """ Palauta tietokannan kirjautumistiedot """
    
    # tietokannan ip, käyttäjänimi ja passu haetaan Secret Managerista
    sql_ip, database, port, user_name, passwd = login_data()

    # kirjautumistiedot sanakirjaan:
    db = {'host': sql_ip, 'database': database, 'port': port, 'user': user_name, 'password': passwd}
    
    return db