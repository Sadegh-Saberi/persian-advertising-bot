import aiosqlite


class DataBase:

    def __init__(self, db: str, table: str, not_update_values: list = None,):
        self.db = db
        self.not_update_values = not_update_values
        self.table = table

    def number_to_gender(self,number: int):
        if number == 0:
            return  "آقا"
        elif number == 1:
            return "خانم"
        elif number == 2:
            return "آقا یا خانم"


    def number_to_term(self,number: int):  # number to work term
        if number == 0:
            return "پاره وقت"
        elif number == 1:
            return "تمام وقت"

    def data_separator(self, data: dict):
        keys_list = list()
        values_list = list()
        for key, value in data.items():
            keys_list.append(key)
            value = f"'{value}'" if type(value) == str else value
            values_list.append(value)

        return [keys_list, values_list]


    async def insert_data(self, data: dict):
        separated_data = self.data_separator(data)
        keys_list, values_list = separated_data
        keys = ", ".join(keys_list)
        question_marks = str("?, "*len(values_list))[:-2]

        async with aiosqlite.connect(self.db) as connection:
            async with connection.cursor() as cursor:
                insert_query = f"INSERT INTO {self.table}({keys}) VALUES({question_marks})"
                await cursor.execute(insert_query, values_list)
                await connection.commit()


    async def update_data(self, user_id: int, key: str, value):
        if value not in self.not_update_values:
            update_query = f""" UPDATE {self.table}
                                SET  {key} = ?  
                                WHERE user_id = ?"""

            async with aiosqlite.connect(self.db) as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(update_query, [value, user_id])
                    await connection.commit()


    async def get_data(self, key, value):
        get_user_data_query = f""" SELECT * FROM {self.table} 
                                  WHERE {key} = ? """

        async with aiosqlite.connect(self.db) as connection:
            async with connection.cursor() as cursor:
                cursor.execute(get_user_data_query, [value])
                data = await cursor.fetchone()
                return data 


    async def delete_data(self, key: str, value):
        delete_query = f""" DELETE FROM {self.table}
                           WHERE {key} = ? """
        async with aiosqlite.connect(self.db) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(delete_query, [value])
                await connection.commit()

async def main():
    async with aiosqlite.connect('DataBase.db') as connection:
        async with connection.cursor() as cursor:
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

# if '__main__' == __name__:
#     await main()
