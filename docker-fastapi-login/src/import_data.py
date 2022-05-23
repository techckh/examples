import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


if __name__ == '__main__':
    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL', None)
    SEED_DATA_DIR = os.getenv('SEED_DATA_DIR', None)
    assert DATABASE_URL, 'error db url'
    assert SEED_DATA_DIR, 'error seed data url'

    """
    columns = [
        'id',
        'email',
        'password',
        'name',
        'created_at'
    ]
    df = pd.read_csv('{}/users.csv'.format(SEED_DATA_DIR), header=None)
    df.columns = columns
    """

    try:
        with open('{}/users.csv'.format(SEED_DATA_DIR), 'r') as f:
            conn = create_engine(DATABASE_URL).raw_connection()
            cursor = conn.cursor()
            cmd = 'COPY users(id, email, password, name, created_at) FROM STDIN WITH (FORMAT CSV, HEADER FALSE)'
            cursor.copy_expert(cmd, f)
            conn.commit()
        print('done')
    except Exception as ex:
        print(ex)

    """
    try:
        engine = create_engine(DATABASE_URL)
    except:
        assert False, 'error db engine'
            
    try:
        with engine.begin() as connection:
            df.to_sql('users', con=connection, index_label='id', if_exists='replace')
    except Exception as ex:
        print(ex)
    """
