from HttpRequest import HttpRequest
from JsonParser import JsonParser
from tkinter import messagebox

class DataParser:
#
    def __init__(self):
        self.data_row_dict = {}
        self.api_data_dict = {}
        self.volume_info_dict = {}
        self.include_google = False
        self.include_worldcat = False
        self.is_google = False
        self.wc_token = ''
        self.included_apis = ''
        self.oclc_symbol = ''
        self.worldcat_connection = None

    def set_wc_access_token(self, token):
        self.wc_token = token

    def clean_return_data(self, element):
        string = str(element)
        cleaned_string = string.replace("',", ",").replace(" '", " ").replace("['", "").replace("']", "")
        return cleaned_string

    def set_oclc_symbol(self, symbol):
        self.oclc_symbol = symbol

    def ol_author_api_request(self, author_key):
       dp_http_request = HttpRequest()
       ol_author_response_bytes = dp_http_request.send_ol_author_request(author_key)
       return ol_author_response_bytes

    def set_book_title(self):
        self.data_row_dict['Title'] = self.api_data_dict.get('title')
        if self.data_row_dict['Title'] != None:
            if self.api_data_dict.get('subtitle') != None:
                self.data_row_dict['Title'] += ": " + self.api_data_dict.get('subtitle')
        if self.data_row_dict['Title'] == None:
            if self.api_data_dict.get('full_title') != None:
                self.data_row_dict['Title'] = self.api_data_dict.get('full_title')
        if self.data_row_dict['Title'] == None and self.include_google:
             self.data_row_dict['Title'] = self.volume_info_dict.get('title')

    def set_book_publisher(self):
        if self.api_data_dict.get('publishers') != None:
            self.data_row_dict['Publisher'] = self.clean_return_data(str(self.api_data_dict.get('publishers')))
        elif self.api_data_dict.get('publishers') == None and self.include_google == True:
            if self.volume_info_dict.get('publisher') != None:
                self.data_row_dict['Publisher'] = self.volume_info_dict.get('publisher')
            else:
                self.data_row_dict['Publisher'] = "Publisher Not Found in Open Library or Google Books"
        else:
            self.data_row_dict['Publisher'] = "Publisher not Found in Open Library"

    def set_book_author(self):
        if self.api_data_dict.get('authors') != None:
            dp_json_parser = JsonParser()
            ol_authors_string = str(self.api_data_dict.get('authors'))
            ol_authors_string = ol_authors_string.replace("{'key': '", "").replace("[", "").replace("'}]", "").replace("'}", "").replace( " ", '')
            ol_authors_list = ol_authors_string.split(",")

            if len(ol_authors_list) > 1:
                names_in_list = ''
                iter = 0
                for author in ol_authors_list:
                    iter = iter + 1
                    author_data_bytes = self.ol_author_api_request(author)
                    if author_data_bytes != False:
                        author_data_dict = dp_json_parser.data_to_python_dict(author_data_bytes)
                        if iter == len(ol_authors_list):
                          names_in_list += author_data_dict['name']
                        else:
                          names_in_list += author_data_dict['name'] + ', '
                    else:
                        names_in_list += "Author name not found"
                name = names_in_list
            else:
                author_data_bytes = self.ol_author_api_request(ol_authors_string)
                if author_data_bytes != False:
                    try:
                        author_data_dict = dp_json_parser.data_to_python_dict(author_data_bytes)
                        name = author_data_dict['name']
                    except:
                        name = 'Author not found in Open Library'
            self.data_row_dict['Author'] = name
        elif self.api_data_dict.get('by_statement') != None:
            self.data_row_dict['Author'] = self.api_data_dict.get('by_statement')
        elif self.api_data_dict.get('contributions') != None:
            ol_contributions_string = str(self.api_data_dict.get('contributions'))
            ol_contributions_string = ol_contributions_string.replace("['", "").replace("']", "").replace("'", "")
            self.data_row_dict['Author'] = ol_contributions_string
        else:
            self.data_row_dict['Author'] = "Author not found in Open Library"

        if self.data_row_dict['Author'] == "Author not found in Open Library" and self.include_google:
            try:
                self.data_row_dict['Author'] = self.volume_info_dict['authors']
            except:
                self.data_row_dict['Author'] = "Author not found in Open Library or Google Books"

    def set_publish_year(self):
        self.data_row_dict['Year Published'] = self.api_data_dict.get('publish_date')

        if self.data_row_dict['Year Published'] == None and self.include_google:
            self.data_row_dict['Year Published'] = self.volume_info_dict.get('publishedDate')

    def set_edition(self):
        self.data_row_dict['Edition'] = self.api_data_dict.get('edition_name')

        if self.data_row_dict['Edition'] == None and self.include_google:
            self.data_row_dict['Edition'] = 'Edition not available in Open Library or Google Books'
        elif self.data_row_dict['Edition'] == None:
            self.data_row_dict['Edition'] = 'Edition not available in Open Library'

    def set_binding(self):
        self.data_row_dict['Binding'] = self.api_data_dict.get('physical_format')

        if self.data_row_dict['Binding'] == None and self.include_google:
            self.data_row_dict['Binding'] = "Binding not found in Open Library.  Google has no binding data"
        elif self.data_row_dict['Binding'] == None:
            self.data_row_dict['Binding'] = "Binding not found in Open Library"

    def set_subjects(self):
        self.data_row_dict['Subjects'] = self.api_data_dict.get('subjects')

        if self.data_row_dict['Subjects'] != None:
            subject_places = self.api_data_dict.get('subject_places')
            if subject_places != None:
                self.data_row_dict['Subjects']. append(subject_places)
        elif self.data_row_dict['Subjects'] == None and self.include_google == False:
            self.data_row_dict['Subjects'] = "No subjects found in Open Library"
        elif self.data_row_dict['Subjects'] == None and self.include_google:
            self.data_row_dict['Subjects'] = "No subjects found in Open Library.  Google Books doesn't offer it"

    def set_dewey_call_number(self):
        self.data_row_dict['Dewey Call Number'] = self.api_data_dict.get('dewey_decimal_class')

        if self.data_row_dict['Dewey Call Number'] != None:
            self.data_row_dict['Dewey Call Number'] = self.clean_return_data(self.data_row_dict['Dewey Call Number'])
        elif self.data_row_dict['Dewey Call Number'] == None and self.include_google == False:
            self.data_row_dict['Dewey Call Number'] = "Dewey call number not found in Open Library"
        elif self.data_row_dict['Dewey Call Number'] == None and self.include_google:
            self.data_row_dict['Dewey Call Number'] = "Dewey call number not found in Open Library.  Google Books doesn't offer it"

    def set_lc_call_number(self):
        self.data_row_dict['LC Call Number'] = self.api_data_dict.get('lc_classifications')

        if self.data_row_dict['LC Call Number'] != None:
            self.data_row_dict['LC Call Number'] = self.clean_return_data(self.data_row_dict['LC Call Number'])
        elif self.data_row_dict['LC Call Number'] == None and self.include_google == False:
            self.data_row_dict['LC Call Number'] = "LC Call Number not found in Open Library"
        elif self.data_row_dict['LC Call Number'] == None and self.include_google:
            self.data_row_dict['LC Call Number'] = "LC Call Number not found in Open Library.  Google Books doesn't offer it"

    def set_pages_number(self):
        self.data_row_dict['Number of Pages'] = self.api_data_dict.get('number_of_pages')

        if self.data_row_dict['Number of Pages'] == None:
            if self.api_data_dict.get('pageCount') != None and self.include_google:
                self.data_row_dict['Number of Pages'] = self.volume_info_dict.get('pageCount')
            elif self.api_data_dict.get('pageCount') == None:
                self.data_row_dict['Number of Pages'] = "Number of Pages not found in Open Library or Google Books"
            else:
                self.data_row_dict['Number of Pages'] = "Number of Pages not found in Open Library"

    def set_oclc_numbers(self):
        self.data_row_dict['OCLC Numbers'] = self.api_data_dict.get('oclc_numbers')

        if self.data_row_dict['OCLC Numbers'] != None:
            self.data_row_dict['OCLC Numbers'] = self.clean_return_data(self.data_row_dict['OCLC Numbers'])
        elif self.data_row_dict['OCLC Numbers'] == None and self.include_google:
            self.data_row_dict['OCLC Numbers'] = "OCLC Numbers not found in Open Library.  Google books doesn't offer it"
        elif self.data_row_dict['OCLC Numbers'] == None:
            self.data_row_dict['OCLC Numbers'] = "OCLC Numbers not found in Open Library"

    def set_record_status(self):
        self.data_row_dict['Record Status'] = self.api_data_dict.get('status')
        if self.data_row_dict['Record Status'] != None and self.include_google == False:
            return False
        elif self.data_row_dict['Record Status'] == None and self.api_data_dict.get('totalItems') == None:
            self.data_row_dict['Record Status'] = "Found in Open Library"
            return True
        elif self.include_google and self.api_data_dict.get('totalItems') == 0:
            self.data_row_dict['Record Status'] = "Not found in Open Library or Google Books"
            return False
        elif self.include_google and self.api_data_dict.get('totalItems') != None:
            self.data_row_dict['Record Status'] = "Found in Google Books"
            return True

    def set_copies_owned(self):
        if self.api_data_dict.get('oclc_numbers') != None:
            oclc = self.clean_return_data(self.api_data_dict.get('oclc_numbers'))
            oclc = oclc.split(',')[0]
            holdings_http_request = HttpRequest()
            holdings_response_bytes = holdings_http_request.send_wc_holdings_request(self.wc_token, oclc, self.oclc_symbol)
            
            if isinstance(holdings_response_bytes, int):
                error_message = "HTTP error of " + str(holdings_response_bytes) + " occured when using OCLC Symbol to make a Worldcat API call.  Check to make sure OCLC Symbol is accurate.  Further API calls to Worldcat will be disabled for this run."
                self.data_row_dict['Number of Copies Owned'] = "OCLC API Authorization Failed"
                messagebox.showinfo("ERROR", error_message)
                self.worldcat_connection = False
                return False
            holdings_json_parser = JsonParser()
            holdings_data_dict = holdings_json_parser.data_to_python_dict(holdings_response_bytes)
            holdings_key_list = list(holdings_data_dict.keys())
            try:
                inst_holdings_dict = holdings_data_dict['briefRecords'][0]['institutionHolding']
                self.data_row_dict['Number of Copies Owned'] = inst_holdings_dict['totalHoldingCount']
            except:
                self.data_row_dict['Number of Copies Owned'] = "OCLC Data not Found"
        else:
            self.data_row_dict['Number of Copies Owned'] = 'OCLC Data not Found'

    def clean_data_row_dict(self):
        for key in self.data_row_dict:
            if self.data_row_dict[key] != None:
                self.data_row_dict[key] = ''

    def set_worldcat_connection(self, boolean):
        self.worldcat_connection = boolean

    def parse_api_data(self, data_dict, row_dict, apis_to_include, current_isbn):
        self.data_row_dict = row_dict
        self.api_data_dict = data_dict
        self.keys_list = list(row_dict.keys())
        self.included_apis = apis_to_include
        if self.included_apis == 'og' or self.included_apis == 'ogw':
            self.include_google = True
        else:
            self.include_google = False
        if self.included_apis == 'ogw':
            self.include_worldcat = True
        else:
            self.include_worldcat = False

        if self.api_data_dict.get('totalItems'):
            self.volume_info_dict = self.api_data_dict['items'][0]['volumeInfo']
            self.is_google = True;
        else:
            self.is_google = False

        for key in self.keys_list:
            if key == 'ISBN':
                self.data_row_dict['ISBN'] = current_isbn
            elif key == 'Record Status':
                if not self.set_record_status():
                    self.data_row_dict['ISBN'] = current_isbn
                    break
            elif key == 'Title':
                self.set_book_title()
            elif key == 'Publisher':
                self.set_book_publisher()
            elif key == 'Author':
                self.set_book_author()
            elif key == 'Year Published':
                self.set_publish_year()
            elif key == 'Edition':
               self.set_edition()
            elif key == 'Binding':
               self.set_binding()
            elif key == 'Number of Pages':
               self.set_pages_number()
            elif key == 'Subjects':
               self.set_subjects()
            elif key == 'Dewey Call Number':
               self.set_dewey_call_number()
            elif key == 'LC Call Number':
               self.set_lc_call_number()
            elif key == 'OCLC Numbers':
               self.set_oclc_numbers()
            elif key == 'Number of Copies Owned' and self.worldcat_connection:
               self.set_copies_owned()
        return self.data_row_dict