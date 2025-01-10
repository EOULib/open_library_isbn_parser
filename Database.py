import sqlite3

class Database:

	def __init__(self):
		self.connection = sqlite3.connect('.app.db')
		self.cursor = self.connection.cursor()
		self.build_tables()
		if self.get_data_save_state() == None and self.get_options_save_state() == None:
			self.cursor.execute("INSERT INTO save_data DEFAULT VALUES")
			self.cursor.execute("INSERT INTO enabled_options DEFAULT VALUES")
			self.cursor.execute("INSERT INTO data_saved_values DEFAULT VALUES")
			self.cursor.execute("INSERT INTO oclc_saved_values DEFAULT VALUES")
			self.connection.commit()

	def build_tables(self):
		self.cursor.execute( """CREATE TABLE IF NOT EXISTS save_data(
            id INTEGER PRIMARY KEY DEFAULT 1,
            data_save_state BOOLEAN DEFAULT False,
            options_save_state BOOLEAN DEFAULT False)""")
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS enabled_options(
			id INTEGER PRIMARY KEY DEFAULT 2,
			google_books_enabled BOOLEAN DEFAULT False,
            worldcat_search_enabled BOOLEAN DEFAULT False)  """)
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS data_saved_values(
			id INTEGER PRIMARY KEY DEFAULT 3,
			title BOOLEAN DEFAULT False,
			author BOOLEAN DEFAULT False,
			publisher BOOLEAN DEFAULT False,
			year_published BOOLEAN DEFAULT False,
			edition BOOLEAN DEFAULT False,
			binding BOOLEAN DEFAULT False,
			lc_subjects BOOLEAN DEFAULT False,
			dewey_call_number BOOLEAN DEFAULT False,
			lc_call_number BOOLEAN DEFAULT False,
			number_of_pages BOOLEAN DEFAULT False,
			oclc_numbers BOOLEAN DEFAULT False)""")
		self.cursor.execute( """CREATE TABLE IF NOT EXISTS oclc_saved_values(
            id INTEGER PRIMARY KEY DEFAULT 4,
            oclc_symbol TEXT DEFAULT '',
            oclc_client_id TEXT DEFAULT '',
            oclc_secret TEXT DEFAULT '')""")

	def get_data_save_state(self):
		data_save_state = self.cursor.execute("SELECT data_save_state FROM save_data;")
		data_save_state = self.cursor.fetchone()
		return data_save_state

	def get_options_save_state(self):
		options_save_state = self.cursor.execute("SELECT options_save_state FROM save_data;")
		options_save_state = self.cursor.fetchone()
		return options_save_state

	def get_table_field_value(self, field, table):
		query = "SELECT " + field + " FROM " + table +";"
		value = self.cursor.execute(query)
		value = self.cursor.fetchone()
		return value[0]

	def set_table_field_value(self, field, table, value):
		query = "UPDATE " + table + " SET " + field + " = ?;"
		self.cursor.execute(query, (value,))
		self.connection.commit()
