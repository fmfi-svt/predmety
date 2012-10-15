
cookie_name = 'predmetysessid'

secret_key = '12345'

session_path = None   # use the default

def db_connect():
    from sqlalchemy import create_engine
    return create_engine('sqlite:///db.sqlite')

