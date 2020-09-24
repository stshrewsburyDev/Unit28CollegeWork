import sqlite3


class DatabaseManager:
    def __init__(self):
        self.DB = sqlite3.connect("data.db", check_same_thread=False)
        self.cursor = self.DB.cursor()

    def get_record(self, id=None):
        query = (id,)
        self.cursor.execute("SELECT * FROM products WHERE ID=?", query)
        return self.cursor.fetchone()

    def get_all_records(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def search(self, args=None):
        records = self.get_all_records()
        if args:
            print(records[0])
            try:
                name = args.get("name")
                records = [record for record in records if name.lower() in record[1].lower()] if name else records
            except ValueError:
                pass
            try:
                type_ = args.get("type")
                if str(type_).lower() in ["cd", "disc"]:
                    type_ = "CD album"
                if str(type_).lower() in ["record", "vinyl", "lp"]:
                    type_ = "Vinyl LP"
                records = [record for record in records if type_.lower() == record[3].lower()] if type_ else records
            except ValueError:
                pass
        return records
