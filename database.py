import sqlite3
import pandas as pd
from PySide6.QtCore import QObject, Signal

class DataManager(QObject):
    """ TODO: Separate these two behavior:
            Changes in the database, needing only UI to be updated
            Changes in what data is selected, needing everything to be updated
    """
    data_changed = Signal()

    def __init__(self, sql_db_path, parent=None):
        super().__init__(parent)

        self.loaded_id = None

        self.sql_conn = sqlite3.connect(sql_db_path)
        self.cursor = self.sql_conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY,
                name TEXT,
                df TEXT
            )
        ''')
        self.sql_conn.commit()

    def select_df(self, new_id):
        self.loaded_id = new_id
        self.data_changed.emit()

    def get_df(self):
        if self.loaded_id is None:
            return None
        data_json = self.cursor.execute('''
            SELECT df
            FROM data
            WHERE id = ?
        ''', (self.loaded_id,)).fetchone()
        if data_json is None:
            return None
        return pd.read_json(data_json[0])

    def get_df_list(self):
        data_json = self.cursor.execute('''
            SELECT id, name, df
            FROM data
        ''').fetchall()
        if not data_json:
            return None
        return data_json

    def save_df(self, data, df_name=""):
        df_json = data.to_json()
        self.cursor.execute('''
            INSERT INTO data (name, df)
            VALUES (?, ?)
        ''', (df_name, df_json))
        self.sql_conn.commit()
        # Notify data changes
        self.data_changed.emit()

    def delete_df(self, id_to_delete):
        self.cursor.execute('''
            DELETE FROM data
            WHERE id = ?
        ''', (id_to_delete,))
        self.sql_conn.commit()
        # Automatically deselect if the deleted df is the current selection
        if self.loaded_id == id_to_delete:
            self.loaded_id = None
        # Notify data changes
        self.data_changed.emit()

