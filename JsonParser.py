import json

class JsonParser:

    def parse_token_response(self, response):
        auth_response_json = json.loads(response)
        access_token = auth_response_json["access_token"]
        return access_token

    def data_to_python_dict(self, api_response):
        api_data_dict = json.loads(api_response)
        return api_data_dict

    def convert_to_json(self, text):
        self.json_convert = json.dumps(text)
        return self.json_convert