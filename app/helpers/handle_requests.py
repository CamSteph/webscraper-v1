# handle_requests.py

import requests
import datetime

class HandleBatchRequests(object):
    """Make HTTP Requests to the endpoint(s) and returns the relevant data.
    """

    def __init__(self) -> None:
        """Constructor
        """
        self.url_endpoints: list[str] = []
        self.all_response_data: list[dict] = []
        self.all_failed_requests: list[dict] = []

    def format_endpoint(self, endpoint) -> str:
        """Append 'http://' to endpoint if it's not present already

        Args:
            endpoint (str): The URL request endpoint

        Returns:
            str: The original endpoint with 'http://' prepended
        """
        if not (endpoint.startswith("http://") or endpoint.startswith("https://")):
            endpoint = "http://" + endpoint
        return endpoint
    
    def set_url_endpoint(self, endpoint : str) -> None:
        """Stores the new URL endponit entered by user

        Args:
            endpoint (str): The endpoint to make the HTTP request to
        """
        self.url_endpoints.append(self.format_endpoint(endpoint))

    def get_all_url_endpoints(self) -> list[str]:
        """Return all entered URL endpoints

        Returns:
            list[str]: List of URL endpoints entered by user
        """
        return self.url_endpoints
    
    def make_standard_get_request(self, endpoint: str) -> None:
        """Initiate GET HTTP request and store the response data

        Args:
            endpoint (str): The endpoint to make the HTTP request to
        """
        try:
            current_time = datetime.datetime.now().strftime("%B %d, %Y - %H:%M:%S")
            response = requests.get(endpoint, verify=True)
            status = response.status_code

            if status >= 200 and status <= 299:
                self.store_response_data({
                    "endpoint": endpoint,
                    "scan_date": current_time,
                    "response_status": status,
                    "response_encoding": response.encoding,
                    "raw_response_headers": response.headers,
                    "response_content": response.text,
                })
            elif status == 301 or status == 302:
                print("The status code is a '%s'" % status)
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            self.all_failed_requests.append({
                "endpoint": endpoint,
                "response_status": status,
                "error_type": f"{type(e).__name__}",
                "full_error": f"{e}",
            })
        except Exception as e:
            print("Something went wrong:")
            print(f"Error type: {type(e).__name__} - {e}")
        
    def store_response_data(self, data) -> None:
        self.all_response_data.append(data)
    
    def get_all_response_data(self) -> list[dict]:
        """Return dictionary of request data

        Returns:
            dict: All request data from previous HTTP requests
        """
        return self.all_response_data
    
    def get_all_failed_requests(self) -> list[dict]:
        """Return dictionary of all failed requests

        Returns:
            dict: All failed requests from attempted HTTP requests
        """
        return self.all_failed_requests