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
        try:
            self.conn = psycopg2.connect(db_conn["db_conn"])
            self.cur = self.conn.cursor()
        except Exception as error:
            print("Oops! An exception has occured:", error)
            print("Exception TYPE:", type(error))

    def write(self, data: dict) -> dict:
        query = f"""
            INSERT INTO user_data (user_id, login_key, password_key, password_salt, created_on)
            VALUES ('{data["user_id"]}', '{data["login_key"]}', '{data["password_key"]}', '{data["password_salt"]}', TIMESTAMP '{data["created_on"]}');
        """

        try:
            self.cur.execute(query)
            self.conn.commit()
            return {"success": True}
        except Exception as error:
            print("Oops! An exception has occured:", error)
            print("Exception TYPE:", type(error))
            return {"success": False}

    def get_user_data(self, user_login: str):
        query = "SELECT user_id, password_key, password_salt FROM user_data"
        f"WHERE login_key = '{user_login}';"

        try:
            self.cur.execute(query)
            result = self.cur.fetchall()  # TODO: make sure that we get result
            return {
                "user_id": result[0][0],
                "password_key": result[0][1],
                "password_salt": result[0][2],
            }
        except Exception as error:
            print("Oops! An exception has occured:", error)
            print("Exception TYPE:", type(error))

    def close(self):
        self.cur.close()
        self.conn.close()
