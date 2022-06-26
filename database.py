from configparser import ConfigParser
import psycopg2


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db


class Database:
    def __init__(self):
        db_conn = config()
        self.conn = psycopg2.connect(db_conn["db_conn"])
        self.cur = self.conn.cursor()

    def write_data(self, data: dict):
        # TODO: how to insert hashed data? https://stackoverflow.com/questions/13683533/hash-a-column-in-postgres-using-sha-256
        query = f"""
            INSERT INTO user_data(user_id, login_key, password_key, password_salt, created_on)
            VALUES ("{data["user_id"]}", "{data["login_key"]}", "{data["password_key"]}", "{data["password_salt"]}", {data["created_on"]})
        """
        self.cur.execute(query)  # TODO: what if an error occurs?

    def close(self):
        self.cur.close()
        self.conn.close()
