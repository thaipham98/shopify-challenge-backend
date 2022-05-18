import sqlite3


class Model:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.handler = self.connection.cursor()
        self.handler.execute('''
            CREATE TABLE IF NOT EXISTS inventories (
                item_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                location TEXT NOT NULL
            );
        ''')
        self.connection.commit()

    def insert(self, inventory):
        inserted_item = {}
        try:
            self.connection = sqlite3.connect("database.db")
            self.handler = self.connection.cursor()
            self.handler.execute("INSERT INTO inventories (name, location) VALUES (?, ?)", (inventory['name'], inventory['location'],))
            self.connection.commit()
            inserted_item = self.get(self.handler.lastrowid)
        except:
            self.connection.rollback()
        finally:
            self.connection.close()

        return inserted_item

    def edit(self, item):
        updated_item = {}
        try:
            self.connection = sqlite3.connect("database.db")
            self.handler = self.connection.cursor()
            self.handler.execute("UPDATE inventories SET name = ?, location = ? WHERE item_id =?",
                                 (item['name'], item['location'], item['item_id'],))
            self.connection.commit()
            updated_item = self.get(item['item_id'])
        except:
            self.connection.rollback()
            updated_item = {}
        finally:
            self.connection.close()

        return updated_item

    def delete(self, item_id):
        message = {}
        try:
            self.connection = sqlite3.connect("database.db")
            self.handler = self.connection.cursor()
            self.handler.execute("DELETE FROM inventories WHERE item_id = ?", (item_id,))
            self.connection.commit()
            message['status'] = "Item deleted successfully"
        except:
            self.connection.rollback()
            message['status'] = "Cannot delete item"
        finally:
            self.connection.close()

        return message

    def list(self):
        items = []
        try:
            self.connection = sqlite3.connect("database.db")
            self.connection.row_factory = sqlite3.Row
            self.handler = self.connection.cursor()
            self.handler.execute("SELECT * FROM inventories")
            rows = self.handler.fetchall()

            for row in rows:
                item = {'item_id': row['item_id'], 'name': row['name'], 'location': row['location']}
                items.append(item)
        except:
            items = []
        return items

    def get(self, item_id):
        item = {}
        try:
            self.connection = sqlite3.connect("database.db")
            self.connection.row_factory = sqlite3.Row
            self.handler = self.connection.cursor()
            self.handler.execute("SELECT * FROM inventories WHERE item_id = ?", (item_id,))
            row = self.handler.fetchone()

            item['item_id'] = row['item_id']
            item['name'] = row['name']
            item['location'] = row['location']
        except:
            item = {}

        return item
