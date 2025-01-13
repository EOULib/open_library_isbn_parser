import csv
from tkinter import messagebox

class CsvHandler:
    def __init__(self):
        self.headings_list = []
        self.list_of_isbns = []
        self.book_row_dict = {}

    def open_import_csv(self, path):
        try:
            with open(path.get(), 'r') as self.import_csv:
                self.csv_reader = csv.DictReader(self.import_csv)
                if self.check_isbn_header() == True:
                    for line in self.csv_reader:
                        self.list_of_isbns.append(line[self.formatted_isbn_key])
                    return "ISBN Found"
                else:
                    return "Check the import csv file and ensure there is a column labeled ISBN"
        except FileNotFoundError as err:
            return "File or Directory Wasn't Found, Click OK and Add a Valid Import File Path"
        except Exception as e:
            return e

    def check_isbn_header(self):
        column_names = self.csv_reader.fieldnames
        uppercase_column_names = [x.upper() for x in column_names]
        required_column_name = 'ISBN'
        if required_column_name in uppercase_column_names:
            for key in column_names:
                isbn_key = str(key)
                if isbn_key.casefold() == required_column_name.casefold():
                    self.formatted_isbn_key = isbn_key
            return True
        else:
            return False

    def get_list_of_isbns(self):
        return self.list_of_isbns

    def set_headings_list(self, list):
        self.headings_list = list

    def create_writeable_csv(self, directory, name):
        self.output_file_name_path = directory.get()+"/"+name.get()
        try:
            self.output_file = open(self.output_file_name_path, 'w', encoding='utf-8-sig')#Must explicitely set encoding to utf-8-sig so that Windows doesn't throw a hissy fit
        except FileNotFoundError as err:
            messagebox.showinfo("ERROR", "Directory Wasn't Found, Click OK and Add a Valid Export Directory Path")
            self.list_of_isbns.clear()
            return False
        except Exception as e:
            messagebox.showinfo("ERROR", e)
            self.list_of_isbns.clear()
            return False
        self.csvwriter = csv.writer(self.output_file)
        self.column_headers = self.headings_list
        self.csvwriter.writerow(self.column_headers)
        return True

    def add_data_row(self, row_list):
        self.csvwriter.writerow(row_list)

    def close_output_file(self):
        self.output_file.close()

    def get_csv_data_dict(self):
        for heading in self.headings_list:
            self.book_row_dict[heading] = ''
        return self.book_row_dict