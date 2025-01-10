from CsvHandler import CsvHandler
from HttpRequest import HttpRequest
from JsonParser import JsonParser
from DataParser import DataParser
from Gui import Gui
from tkinter import messagebox
import threading
import time
import os

class Controller:
    def __init__(self):
        self.csv_handler = CsvHandler()
        self.http_request = HttpRequest()
        self.json_parser = JsonParser()
        self.data_parser = DataParser()
        self.gui = Gui()
        self.program_running = True
        self.while_loop_thread = threading.Thread(target=self.start_program_loop)
        self.while_loop_thread.start()
        self.gui.window.protocol("WM_DELETE_WINDOW", self.close_program_loop)
        self.gui.start_interface()
        
    def start_program_loop(self):
        while self.program_running:
            time.sleep(0.25)
            if self.check_run_button_press():
                self.run_parser()
            self.gui.set_run_btn_pushed_false()

    def close_program_loop(self):
        self.program_running = False
        self.gui.stop_interface()

    def check_run_button_press(self):
        run_button_state = self.gui.get_run_btn_state()
        return run_button_state

    def window_state(self):
        state = self.gui.check_window_state()
        return state

    def handle_import_file(self):
        import_file_path = self.gui.get_import_file()
        import_csv = self.csv_handler.open_import_csv(import_file_path)
        if import_csv !="ISBN Found":
            messagebox.showinfo("ERROR", import_csv)
            return False
        column_headings_list = self.gui.get_column_headings()
        self.csv_handler.set_headings_list(column_headings_list)
        return True

    def run_parser(self):
        self.gui.change_run_button_state('disabled')
        if self.gui.get_import_file().get() == '':
            messagebox.showinfo("ERROR", "Path to input file is a required field.  Click Okay and enter a valid directory path and file name.")
            self.gui.change_run_button_state('normal')
            return False
        if not self.handle_import_file():
            self.gui.change_run_button_state('normal')
            return False

        isbn_list = self.csv_handler.get_list_of_isbns()
        self.api_includes = self.gui.get_api_includes()
        row_data_dict = self.csv_handler.get_csv_data_dict()

        output_directory = self.gui.get_output_directory()
        if output_directory.get() == '':
            messagebox.showinfo("ERROR", "Directory to save export is a required field.  Click Okay and enter a valid directory path.")
            self.gui.change_run_button_state('normal')
            isbn_list.clear()
            return False
        
        output_file_name = self.gui.get_output_file_name()
        if output_file_name.get() == '':
            messagebox.showinfo("ERROR", "Name for export CSV is a required field.  Click Okay and enter a name for the export file.")
            isbn_list.clear()
            self.gui.change_run_button_state('normal')
            return False
        substring = output_file_name.get()
        if substring[-4:] != '.csv':
            fullstring = substring + '.csv'
            output_file_name.set(fullstring)
        
        if not self.csv_handler.create_writeable_csv(output_directory, output_file_name):
            self.gui.change_run_button_state('normal')
            return False
        
        if self.api_includes == 'ogw' or self.api_includes == 'ow':
            oclc_symbol = self.gui.get_oclc_symbol()
            if oclc_symbol.get() == '':
                messagebox.showinfo("ERROR", "OCLC Symbol is a required field.  Click Okay and enter a valid OCLC Symbol before running the parser again. Or uncheck the Enable OCLC API box to stop searching Worldcat")
                self.gui.change_run_button_state('normal')
                self.csv_handler.close_output_file()
                os.remove(output_file_name.get())
                isbn_list.clear()
                return False
            self.data_parser.set_oclc_symbol(oclc_symbol)
            client_id = self.gui.get_client_id()
            if client_id.get() == '':
                messagebox.showinfo("ERROR", "Client ID is a required field.  Click Okay and enter a valid Client ID before running the parser again. Or uncheck the Enable OCLC API box to stop searching Worldcat")
                self.gui.change_run_button_state('normal')
                self.csv_handler.close_output_file()
                os.remove(output_file_name.get())
                return False
            client_secret = self.gui.get_client_secret()
            if client_secret.get() == '':
                messagebox.showinfo("ERROR", "Secret is a required field.  Click Okay and enter a valid Secret before running the parser again. Or uncheck the Enable OCLC API box to stop searching Worldcat")
                self.gui.change_run_button_state('normal')
                isbn_list.clear()
                self.csv_handler.close_output_file()
                os.remove(output_file_name.get())
                return False
            auth_key = self.http_request.encode_wc_auth_key(client_id.get(), client_secret.get())
            token_data = self.http_request.request_wc_token(auth_key)
            if isinstance(token_data, int):
                error_message = "HTTP error of " + str(token_data) + " occured when using Client ID and Secret to make a Worldcat API call.  Check to make sure Client ID and Secret are accurate and approved by OCLC.  Further API calls to Worldcat will be disabled for this run."
                messagebox.showinfo("ERROR", error_message)
                self.data_parser.set_worldcat_connection(False)
            else:
                self.data_parser.set_worldcat_connection(True)
                token =self.json_parser.parse_token_response(token_data)
                self.data_parser.set_wc_access_token(token)

        number_of_records = len(isbn_list)
        records_processed = 0
        progress_thread = threading.Thread(target=self.gui.start_progressbar)

        for isbn in isbn_list:
            records_processed += 1
            self.data_parser.clean_data_row_dict()
            response_bytes = self.http_request.send_api_get_request(isbn, self.api_includes)
            if response_bytes != False:
                response_dict = self.json_parser.data_to_python_dict(response_bytes)
            else:
                response_dict = {'status': 'Book Not Found in Open Library'}
            row_dict = self.data_parser.parse_api_data(response_dict, row_data_dict, self.api_includes, isbn)
            row_list = list(row_dict.values())
            self.csv_handler.add_data_row(row_list)
            row_list.clear()
            increment_by = records_processed/number_of_records 
            self.gui.update_progressbar(number_of_records, records_processed)
        self.gui.stop_progressbar(number_of_records)
        self.gui.change_run_button_state('normal')
        self.csv_handler.close_output_file()
        isbn_list.clear()