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


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self):
        db_conn = config()
        try:
            self.conn = psycopg2.connect(db_conn["db_conn"])
            self.cur = self.conn.cursor()
        except Exception as error:
            print("Oops! An exception has occured:", error)
            print("Exception TYPE:", type(error))

    def execute(self, query: str, result=False):
        try:
            self.cur.execute(query)
            if result:
                # TODO: make sure that we get result
                data = self.cur.fetchall()
                return data
            else:
                return {"success": True}
        except Exception as error:
            print("Oops! An exception has occured:", error)
            print("Exception TYPE:", type(error))
            self.conn.rollback()
            return {"success": False}

    def close(self):
        self.cur.close()
        self.conn.close()
