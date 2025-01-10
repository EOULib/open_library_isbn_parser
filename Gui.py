import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.ttk import Style
from tkinter.constants import DISABLED, NORMAL
from tkinter import messagebox

from Clipboard import Clipboard
from Database import Database
from Progressbar import Progressbar


class Gui:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Book Data by ISBN")
		self.window.resizable(True, True)
		self.window.minsize(980, 825)
		self.window.maxsize(1920, 1080)
		self.run_button_pushed = False
		self.database = Database()
		self.window.columnconfigure(0, weight=1)
		self.window.rowconfigure(0, weight=1)
		self.window.rowconfigure(4, weight=1)
		self.build_mainframe()
		self.build_header_frame()
		self.build_file_frame()
		self.build_data_frame()
		self.build_optional_frame()
		self.build_bottom_frame()

	def start_interface(self):
		self.window.mainloop()

	def stop_interface(self):
		self.window.quit()

	def check_window_state(self):
		return self.window.winfo_exists()

	def open_file(self):
		file_path = filedialog.askopenfilename(filetypes=(("csv files", "*.csv"),))
		self.file_import_value.set(file_path)

	def select_directory(self):
		directory_path = filedialog.askdirectory(title="Choose the directory to save to")
		self.file_export_value.set(directory_path)

	def get_import_file(self):
		file_path_str = self.file_import_value
		return file_path_str

	def get_column_headings(self):
		checkbutton_list = ["ISBN", "Record Status"]
		if self.title_checkbutton_checked.get():
			checkbutton_list.append("Title")
		if self.author_checkbutton_checked.get():
			checkbutton_list.append("Author")
		if self.publisher_checkbutton_checked.get():
			checkbutton_list.append("Publisher")
		if self.year_checkbutton_checked.get():
			checkbutton_list.append("Year Published")
		if self.edition_checkbutton_checked.get():
			checkbutton_list.append("Edition")
		if self.binding_checkbutton_checked.get():
			checkbutton_list.append("Binding")
		if self.subjects_checkbutton_checked.get():
			checkbutton_list.append("Subjects")
		if self.dewey_checkbutton_checked.get():
			checkbutton_list.append("Dewey Call Number")
		if self.lc_checkbutton_checked.get():
			checkbutton_list.append("LC Call Number")
		if self.pages_checkbutton_checked.get():
			checkbutton_list.append("Number of Pages")
		if self.oclc_checkbutton_checked.get():
			checkbutton_list.append("OCLC Numbers")
		if self.select_oclc_option_checked.get():
			checkbutton_list.append("Number of Copies Owned")

		return checkbutton_list

	def get_oclc_symbol(self):
		return self.oclc_symbol_value

	def get_client_id(self):
		return self.client_id_value

	def get_client_secret(self):
		return self.client_secret_value

	def set_run_btn_pushed_true(self):
		self.run_button_pushed = True

	def set_run_btn_pushed_false(self):
		self.run_button_pushed = False 

	def get_run_btn_state(self):
		return self.run_button_pushed

	def set_oclc_options_state(self):
		if self.select_oclc_option_checked.get():
			self.oclc_symbol_entry['state'] = 'normal'
			self.client_id_entry['state'] = 'normal'
			self.client_secret_entry['state'] = 'normal'
		else:
			self.oclc_symbol_entry['state'] = 'disabled'
			self.client_id_entry['state'] = 'disabled'
			self.client_secret_entry['state'] = 'disabled'

	def get_api_includes(self):
		if self.select_oclc_option_checked.get() and self.google_books_backup_checked.get():
			api_includes = 'ogw'
		elif self.google_books_backup_checked.get():
			api_includes = 'og'
		elif self.select_oclc_option_checked.get():
			api_includes = 'ow'
		else:
			api_includes = 'o'
		return api_includes

	def get_output_directory(self):
		return self.file_export_value

	def get_output_file_name(self):
		return self.export_file_name_value

	def save_data_configs(self):
		data_config_dict = {
			'title': self.title_checkbutton_checked.get(),
			'author': self.author_checkbutton_checked.get(),
			'publisher': self.publisher_checkbutton_checked.get(),
			'year_published': self.year_checkbutton_checked.get(),
			'edition': self.edition_checkbutton_checked.get(),
			'binding': self.binding_checkbutton_checked.get(),
			'lc_subjects': self.subjects_checkbutton_checked.get(),
			'dewey_call_number': self.dewey_checkbutton_checked.get(),
			'lc_call_number': self.lc_checkbutton_checked.get(),
			'number_of_pages': self.pages_checkbutton_checked.get(),
			'oclc_numbers': self.oclc_checkbutton_checked.get()
		}

		for field in data_config_dict:
			self.database.set_table_field_value(field, 'data_saved_values', data_config_dict.get(field))
		messagebox.showinfo("Saved Configuration", "Data configurations have been saved")

	def save_options_configs(self):
		options_enabled_dict = {
			'google_books_enabled': self.google_books_backup_checked.get(),
			'worldcat_search_enabled': self.select_oclc_option_checked.get()
		}
		for field in options_enabled_dict:
			self.database.set_table_field_value(field, 'enabled_options', options_enabled_dict.get(field))

		oclc_api_dict = {
			'oclc_symbol': self.oclc_symbol_value.get(),
			'oclc_client_id': self.client_id_value.get(),
			'oclc_secret': self.client_secret_value.get()
		}
		for field in oclc_api_dict:
			self.database.set_table_field_value(field, 'oclc_saved_values', oclc_api_dict.get(field))

		messagebox.showinfo("Saved Configuration", "Optional configurations have been saved")

	def build_mainframe(self):
		self.main_frame = ttk.Frame(self.window)
		self.main_frame.grid(row=0, column=0, padx=5, pady=5, sticky='new')
		self.main_frame.columnconfigure(0, weight=1)
		self.main_frame.rowconfigure(0, weight=1)

	def build_header_frame(self):
		header_frame = ttk.Frame(self.main_frame)
		header_frame.grid(row=0, column=0, sticky='nsew')
		header_frame.columnconfigure(0, weight=1)
		header_frame.columnconfigure(1, weight=1)
		header_frame.columnconfigure(2, weight=1)

		header_label = ttk.Label(header_frame, text="Open Library ISBN Parser", font=('Arial', 22))
		header_label.grid(row=0, column=1, padx=20, pady=20)

	def build_file_frame(self):
		file_frame = ttk.Frame(self.main_frame, borderwidth=1, relief="solid")
		file_frame.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
		file_frame.columnconfigure(0, weight=0)
		file_frame.columnconfigure(1, weight=2)
		file_frame.columnconfigure(2, weight=0)

		file_label = ttk.Label(file_frame, text="File Configurations", font=('Arial', 18, "underline"))
		file_label.grid(row=0, column=0, padx=5, pady=15, sticky='w')
		
		input_file_label = ttk.Label(file_frame, text="Path to Import File:", font=('Arial', 14))
		input_file_label.grid(row=1, column=0, padx=(50, 10), pady=5, sticky='w')
		self.file_import_value = tk.StringVar()
		file_import_entry = ttk.Entry(file_frame, textvariable=self.file_import_value)
		input_file_clipboard = Clipboard()
		input_file_clipboard.add_menu(self.window, file_import_entry, self.file_import_value)
		file_import_entry.grid(row=1, column=1, sticky='ew')
		file_import_browse = ttk.Button(file_frame, width=15, text="Find File", command=self.open_file)
		file_import_browse.grid(row=1, column=2, padx=10, pady=5)

		export_file_label = ttk.Label(file_frame, text="Directory to Save Export:", font=('Arial', 14))
		export_file_label.grid(row=2, column=0, padx=(50, 10), pady=5, sticky='w')
		self.file_export_value = tk.StringVar()
		file_export_entry = ttk.Entry(file_frame, textvariable=self.file_export_value)
		export_file_clipboard = Clipboard()
		export_file_clipboard.add_menu(self.window, file_export_entry, self.file_export_value)
		file_export_entry.grid(row=2, column=1, sticky='ew')
		file_export_browse = ttk.Button(file_frame, width=15, text="Select Directory", command=self.select_directory)
		file_export_browse.grid(row=2, column=2, padx=10, pady=5)

		export_file_name_label = ttk.Label(file_frame, text="Name for Output CSV:", font=('Arial', 14))
		export_file_name_label.grid(row=3, column=0, padx=(50, 10), pady=(5,15), sticky='w')
		self.export_file_name_value = tk.StringVar()
		export_file_name_entry = ttk.Entry(file_frame, textvariable=self.export_file_name_value)
		export_name_clipboard = Clipboard()
		export_name_clipboard.add_menu(self.window, export_file_name_entry, self.export_file_name_value)
		export_file_name_entry.grid(row=3, column=1, sticky="ew")

	def build_data_frame(self):
		data_frame = ttk.Frame(self.main_frame, borderwidth=1, relief="solid")
		data_frame.grid(row=2, column=0, padx=10, pady=15, sticky='nsew')
		data_frame.columnconfigure(0, weight=1)
		data_frame.columnconfigure(1, weight=1)
		data_frame.columnconfigure(2, weight=1)
		data_frame.columnconfigure(3, weight=1)
		data_frame.columnconfigure(4, weight=1)

		data_label = ttk.Label(data_frame, text="Data Configurations", font=('Arial', 18, "underline"))
		data_label.grid(row=0, columnspan=2, padx=5, pady=10, sticky='w')
		data_instructions_label = ttk.Label(data_frame, text="*Select data points below to output to CSV")
		data_instructions_label.grid(row=0, column=2, columnspan=2, padx=5, pady=10, sticky='w')
		save_data_button = ttk.Button(data_frame, width=17, text="Save Configurations", command=self.save_data_configs)
		save_data_button.grid(row=0, column=4, padx=10, pady=5)

		data_checkbutton_style = Style()
		data_checkbutton_style.configure("cb.TCheckbutton", font=('Arial', 14))

		self.title_checkbutton_checked = tk.BooleanVar()
		self.title_checkbutton_checked.set(self.database.get_table_field_value('title', 'data_saved_values'))
		title_checkbutton = ttk.Checkbutton(data_frame, text="Title", style="cb.TCheckbutton", variable=self.title_checkbutton_checked)
		title_checkbutton.grid (row=2, column=1, padx=(50, 0), pady=5, sticky='we')

		self.author_checkbutton_checked = tk.BooleanVar()
		self.author_checkbutton_checked.set(self.database.get_table_field_value('author', 'data_saved_values'))
		author_checkbutton = ttk.Checkbutton(data_frame, text="Author", style="cb.TCheckbutton", variable=self.author_checkbutton_checked)
		author_checkbutton.grid (row=2, column=2, sticky='we')

		self.publisher_checkbutton_checked = tk.BooleanVar()
		self.publisher_checkbutton_checked.set(self.database.get_table_field_value('publisher', 'data_saved_values'))
		publisher_checkbutton = ttk.Checkbutton(data_frame, text="Pulisher", style="cb.TCheckbutton", variable=self.publisher_checkbutton_checked)
		publisher_checkbutton.grid (row=2, column=3, sticky='we')

		self.year_checkbutton_checked = tk.BooleanVar()
		self.year_checkbutton_checked.set(self.database.get_table_field_value('year_published', 'data_saved_values'))
		year_checkbutton = ttk.Checkbutton(data_frame, text="Year Published", style="cb.TCheckbutton", variable=self.year_checkbutton_checked)
		year_checkbutton.grid (row=2, column=4, sticky='we')

		self.edition_checkbutton_checked = tk.BooleanVar()
		self.edition_checkbutton_checked.set(self.database.get_table_field_value('edition', 'data_saved_values'))
		edition_checkbutton = ttk.Checkbutton(data_frame, text="Edition", style="cb.TCheckbutton", variable=self.edition_checkbutton_checked)
		edition_checkbutton.grid (row=3, column=1, padx=(50, 0), pady=5, sticky='we')

		self.binding_checkbutton_checked = tk.BooleanVar()
		self.binding_checkbutton_checked.set(self.database.get_table_field_value('binding', 'data_saved_values'))
		binding_checkbutton = ttk.Checkbutton(data_frame, text="Binding", style="cb.TCheckbutton", variable=self.binding_checkbutton_checked)
		binding_checkbutton.grid (row=3, column=2, sticky='we')

		self.subjects_checkbutton_checked = tk.BooleanVar()
		self.subjects_checkbutton_checked.set(self.database.get_table_field_value('lc_subjects', 'data_saved_values'))
		subjects_checkbutton = ttk.Checkbutton(data_frame, text="LC Subjects", style="cb.TCheckbutton", variable=self.subjects_checkbutton_checked)
		subjects_checkbutton.grid (row=3, column=3, sticky='we')

		self.dewey_checkbutton_checked = tk.BooleanVar()
		self.dewey_checkbutton_checked.set(self.database.get_table_field_value('dewey_call_number', 'data_saved_values'))
		dewey_checkbutton = ttk.Checkbutton(data_frame, text="Dewey Call Number", style="cb.TCheckbutton", variable=self.dewey_checkbutton_checked)
		dewey_checkbutton.grid (row=3, column=4, sticky='we')

		self.lc_checkbutton_checked = tk.BooleanVar()
		self.lc_checkbutton_checked.set(self.database.get_table_field_value('lc_call_number', 'data_saved_values'))
		lc_checkbutton = ttk.Checkbutton(data_frame, text="LC Call Number", style="cb.TCheckbutton", variable=self.lc_checkbutton_checked)
		lc_checkbutton.grid (row=4, column=1, padx=(50, 0), pady=(5, 15), sticky='we')

		self.pages_checkbutton_checked = tk.BooleanVar()
		self.pages_checkbutton_checked.set(self.database.get_table_field_value('number_of_pages', 'data_saved_values'))
		pages_checkbutton = ttk.Checkbutton(data_frame, text="Number of Pages", style="cb.TCheckbutton", variable=self.pages_checkbutton_checked)
		pages_checkbutton.grid (row=4, column=2, sticky='we')

		self.oclc_checkbutton_checked = tk.BooleanVar()
		self.oclc_checkbutton_checked.set(self.database.get_table_field_value('title', 'data_saved_values'))
		oclc_checkbutton = ttk.Checkbutton(data_frame, text="OCLC Numbers", style="cb.TCheckbutton", variable=self.oclc_checkbutton_checked)
		oclc_checkbutton.grid (row=4, column=3, sticky='we')

	def build_optional_frame(self):
		optional_frame = ttk.Frame(self.main_frame, borderwidth=1, relief="solid")
		optional_frame.grid(row=3, column=0, padx=10, pady=15, sticky='nsew')
		optional_frame.columnconfigure(0, weight=1)
		optional_frame.columnconfigure(1, weight=2)
		optional_frame.columnconfigure(2, weight=45)

		optional_label = ttk.Label(optional_frame, text="Optional Configurations", font=('Arial', 18, "underline"))
		optional_label.grid(row=0, columnspan=2, padx=5, pady=10, sticky='w')
		save_options_button = ttk.Button(optional_frame, width=17, text="Save Options", command=self.save_options_configs)
		save_options_button.grid(row=0, column=2, padx=(10, 30), pady=5, sticky='e')

		optional_checkbutton_style = Style()
		optional_checkbutton_style.configure("cb.TCheckbutton", font=('Arial', 14))
		
		self.google_books_backup_checked = tk.BooleanVar()
		self.google_books_backup_checked.set(self.database.get_table_field_value('google_books_enabled', 'enabled_options'))
		google_books_backup = ttk.Checkbutton(optional_frame, text="Enable Backup Google Books API", style="cb.TCheckbutton", variable=self.google_books_backup_checked)
		google_books_backup.grid(row=1, column=0, padx=(50, 0), pady=5, sticky='we')

		self.select_oclc_option_checked = tk.BooleanVar()
		self.select_oclc_option_checked.set(self.database.get_table_field_value('worldcat_search_enabled', 'enabled_options'))
		select_oclc_option = ttk.Checkbutton(optional_frame, text="Enable OCLC API to Check Local Holdings", 
			variable=self.select_oclc_option_checked, style="cb.TCheckbutton", command=self.set_oclc_options_state)
		select_oclc_option.grid(row=1, column=1, columnspan=2, padx=(50, 5), pady=5, sticky='we')

		oclc_symbol_label = ttk.Label(optional_frame, text="OCLC Symbol:", font=('Arial', 14))
		oclc_symbol_label.grid(row=2, column=1, padx=(50, 5), pady=5, sticky='e')
		self.oclc_symbol_value = tk.StringVar()
		self.oclc_symbol_value.set(self.database.get_table_field_value('oclc_symbol', 'oclc_saved_values'))
		self.oclc_symbol_entry = ttk.Entry(optional_frame, textvariable=self.oclc_symbol_value)
		oclc_symbol_clipboard = Clipboard()
		oclc_symbol_clipboard.add_menu(self.window, self.oclc_symbol_entry, self.oclc_symbol_value)
		self.oclc_symbol_entry.grid(row=2, column=2, padx=(0, 20), pady=5, sticky="we")

		client_id_label = ttk.Label(optional_frame, text="Client ID:", font=('Arial', 14))
		client_id_label.grid(row=3, column=1, padx=(70, 5), pady=5, sticky='e')
		self.client_id_value = tk.StringVar()
		self.client_id_value.set(self.database.get_table_field_value('oclc_client_id', 'oclc_saved_values'))
		self.client_id_entry = ttk.Entry(optional_frame, textvariable=self.client_id_value)
		client_id_clipboard = Clipboard()
		client_id_clipboard.add_menu(self.window, self.client_id_entry, self.client_id_value)
		self.client_id_entry.grid(row=3, column=2, padx=(0, 20), pady=5, sticky="we")

		client_secret_label = ttk.Label(optional_frame, text="Secret:", font=('Arial', 14))
		client_secret_label.grid(row=4, column=1, padx=(80, 5), pady=(5, 10), sticky='e')
		self.client_secret_value = tk.StringVar()
		self.client_secret_value.set(self.database.get_table_field_value('oclc_secret', 'oclc_saved_values'))
		self.client_secret_entry = ttk.Entry(optional_frame, textvariable=self.client_secret_value)
		client_secret_clipboard = Clipboard()
		client_secret_clipboard.add_menu(self.window, self.client_secret_entry, self.client_secret_value)
		self.client_secret_entry.grid(row=4, column=2, padx=(0, 20), pady=(5, 10), sticky="we")

		self.set_oclc_options_state()

	def build_bottom_frame(self):
		bottom_frame = ttk.Frame(self.main_frame)
		bottom_frame.grid(row=4, column=0, sticky='nsew')
		bottom_frame.columnconfigure(0, weight=1)
		bottom_frame.columnconfigure(1, weight=1)
		bottom_frame.columnconfigure(2, weight=1)

		run_button_style = ttk.Style()
		run_button_style.configure('run.TButton', font=('Arial', 14))
		self.run_button = ttk.Button(bottom_frame, text="Run Parser", width=30, style='run.TButton', command=self.set_run_btn_pushed_true)
		self.run_button.grid(row=0, column=1, padx=20, pady=20)

		self.progressbar = Progressbar(bottom_frame)

	def change_run_button_state(self, state):
		self.run_button['state'] = state

	def start_progressbar(self):
		self.progressbar.start_display()

	def update_progressbar(self, number_of_records, record_number):
		self.progressbar.update_display(number_of_records, record_number)

	def stop_progressbar(self, number_of_records):
		self.progressbar.stop_display(number_of_records)