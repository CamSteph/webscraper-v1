# handle_request_data.py

import json

class HandleRequestData(object):
    def __init__(self, request_data):
        self.request_data = request_data
    
    def format_data(self, data) -> str:
        try:
            return data
            return json.dumps(data, indent=4)
        except Exception as e:
            print(e)

    def get_data(self) -> str:
        return self.format_data(self.request_data)