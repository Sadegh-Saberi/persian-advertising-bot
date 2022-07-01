import sqlite3
import aiosqlite


class DataBase:

    def __init__(self, db: str, table: str, not_update_values: list = None,):
        self.db = db
        self.not_update_values = not_update_values
        self.table = table

    def number_to_gender(number: int):
        if number == 0:
            return 'آقا'
        elif number == 1:
            return 'خانم'
        elif number == 2:
            return 'آقا یا خانم'

    def number_to_term(number: int):  # number to work term
        if number == 0:
            return 'پاره وقت'
        elif number == 1:
            return 'تمام وقت'

    def data_separator(self, data: dict):
        keys_list = list()
        values_list = list()
        for key, value in data.items():
            keys_list.append(key)
            value = f"'{value}'" if type(value) == str else value
            values_list.append(value)

        return [keys_list, values_list]
    # inserting the temporary data

    async def insert_data(self, data: dict):  # insert_temp_data ###
        connection = await aiosqlite.connect(self.db)
        cursor = await connection.cursor()
        separated_data = self.data_separator(data)
        keys_list, values_list = separated_data
        keys = ", ".join(keys_list)
        question_marks = str("?, "*len(values_list))[:-2]
        insert_query = f"INSERT INTO {self.table}({keys}) VALUES({question_marks})"
        await cursor.execute(insert_query, values_list)

        await connection.commit()
        await connection.close()

    # it gives a list containing 2 items, the first item is the variable in the database and the second item is the new value of the variable.

    async def update_data(self, user_id: int, key: str, value):  # update_temp_data ###
        if value not in self.not_update_values:
            connection = await aiosqlite.connect(self.db)
            cursor = await connection.cursor()
            await connection.commit()
            update_query = f""" UPDATE {self.table}
                                SET  {key} = ?  
                                WHERE user_id = ?"""
            await cursor.execute(update_query, [value, user_id])
            await connection.commit()
            await connection.close()

    async def get_data(self, key, value):  # get data
        connection = await aiosqlite.connect(self.db)
        cursor = await connection.cursor()
        get_user_data_query = f""" SELECT * FROM {self.table} 
                                  WHERE {key} = ? """
        await cursor.execute(get_user_data_query, [value])
        data = await cursor.fetchone()
        await connection.close()
        return data

    # delete user temp data / delete user final data
    async def delete_data(self, key: str, value):
        connection = await aiosqlite.connect(self.db)
        cursor = await connection.cursor()
        delete_query = f""" DELETE FROM {self.table}
                           WHERE {key} = ? """
        await cursor.execute(delete_query, [value])
        await connection.commit()
        await connection.close()


if '__main__' == __name__:
    connection = sqlite3.connect('DataBase.db')
    cursor = connection.cursor()
    query = """CREATE TABLE adv(
                user_id  INTEGER PRIMARY KEY,
                title TEXT,
                gender INTEGER,
                term INTEGER,
                education TEXT,
                experience TEXT,
                time TEXT,
                age TEXT,
                advantages TEXT,
                contact TEXT,
                photo BLOB
                )
            """ # add income TEXT
            # add explanation TEXT

    cursor.execute(query)
    connection.commit()
    query = """ CREATE TABLE final_adv(
                user_id INTEGER PRIMARY KEY,
                caption TEXT,
                photo BLOB
                )
            """
    cursor.execute(query)
    connection.commit()

    query = """ CREATE TABLE project(
                user_id INTEGER PRIMARY KEY,
                title TEXT,
                explanation TEXT,
                budget TEXT,
                contact TEXT
                )
            """
    cursor.execute(query)
    connection.commit()

    query = """ CREATE TABLE final_project(
                user_id INTEGER PRIMARY KEY,
                text BLOB
                )
            """
    cursor.execute(query)
    connection.commit()

    query = """ CREATE TABLE service(
                user_id INTEGER PRIMARY KEY,
                title TEXT,
                skills TEXT,
                explanation BLOB,
                contact TEXT,
                photo BLOB
                )
            """
    cursor.execute(query)
    connection.commit()
    query = """ CREATE TABLE final_service(
                user_id INTEGER PRIMARY KEY,
                caption BLOB,
                photo BLOB
                )
            """
    cursor.execute(query)
    connection.commit()
    connection.close()
