import urllib3 

from http.client import responses
import base64
import time

class HttpRequest:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.ol_api_url = 'https://openlibrary.org/isbn/'
        self.google_api_url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'
        self.api_headers = {
            'User-Agent': 'BookDataByIsbn/1.0 (jkellogg@eou.edu)'
        }
        self.wc_auth_url = 'https://oauth.oclc.org/token?grant_type=client_credentials&scope=wcapi'
        self.wc_api_url = 'https://americas.discovery.api.oclc.org/worldcat/search/v2/bibs-holdings?heldBySymbol='

    def send_wc_holdings_request(self, token, oclc_number, symbol):
        holdings_headers = {
            'Authorization': 'Bearer ' + token
        }
        holdings_data_request = self.http.request(
            'GET',
            self.wc_api_url + symbol.get() + '&oclcNumber=' + str(oclc_number),
            headers = holdings_headers
        )
        http_status = holdings_data_request.status
        if http_status == 200:
            return holdings_data_request.data
        else:
            return http_status

    def send_ol_author_request(self, author_key):
        ol_author_api_url = 'https://openlibrary.org' + author_key + '.json'
        get_author_info = self.http.request(
                 "GET",
                 ol_author_api_url,
                 headers = self.api_headers
            )
        http_status = get_author_info.status
        if http_status == 200:
            return get_author_info.data
        elif http_status == 429:
            loop_state = True
            iterator = 0
            while loop_state == True:
                time.sleep(7)
                get_author_info = self.http.request(
                    "GET",
                    ol_author_api_url,
                    headers = self.api_headers
                )
                http_status = get_author_info.status
                if http_status == 200:
                    loop_state = False
                    return http_status
                elif iterator = 10:
                    return False
        else:
            return False

    def send_api_get_request(self, isbn, apis):
        where_to_search = apis
        self.get_request = self.http.request(
                "GET",
                self.ol_api_url + isbn + '.json',
                headers = self.api_headers
            )
        http_status = self.get_request.status
        if http_status == 200:
            return self.get_request.data
        elif where_to_search == 'og' or where_to_search == 'ogw':
            self.google_get_request = self.http.request(
                "GET",
                 self.google_api_url + isbn,
                 headers = self.api_headers
            )
            return self.google_get_request.data
        else:
            return False

    def encode_wc_auth_key(self, client_id, client_secret):
        auth_combo_key = client_id + ":" + client_secret
        auth_combo_key_bytes = auth_combo_key.encode("utf-8")
        auth_combo_key_b64 = base64.b64encode(auth_combo_key_bytes)
        return auth_combo_key_b64.decode("utf-8")

    def request_wc_token(self, auth_key):
        auth_headers = {
            'Accept': 'application/json',
            'Authorization': 'Basic ' + auth_key,
            'Content-Length': '0'
        }
        post_request = self.http.request(
            "POST",
            self.wc_auth_url,
            headers = auth_headers
        )
        http_status = post_request.status
        if http_status == 200:
            return post_request.data
        else:
            return http_status