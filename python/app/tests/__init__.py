from ..common.database_utils import DatabaseManager


try:
    DatabaseManager.get_database()
except BaseException as error:
    print("Error connecting to database : {}".format(error))
