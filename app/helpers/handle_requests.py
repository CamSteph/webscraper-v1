# handle_requests.py

from idna import decode
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
        status = None
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
                    "full_response_content": response.text,
                    "found_script_tags": self._find_script_tags(response.text),
                    "found_hyperlinks": self._find_hyperlinks(response.text),
                })
            elif status == 301 or status == 302:
                print("The status code is a '%s'" % status)
            else:
                response.raise_for_status()
        except requests.exceptions.Timeout as e:
            self.add_failed_request(endpoint, status, e)
        except requests.RequestException as e:
            self.add_failed_request(endpoint, status, e)
        except Exception as e:
            self.add_failed_request(endpoint, status, e)
        
    def store_response_data(self, data) -> None:
        """Save response data from HTTP request in a list

        Args:
            data (dict): The response data from the HTTP request
        """
        self.all_response_data.append(data)
    
    def get_all_response_data(self) -> list[dict]:
        """Return dictionary of request data

        Returns:
            dict: All request data from previous HTTP requests
        """
        return self.all_response_data
    
    def add_failed_request(self, endpoint, status, error) -> None:
        """Add failed HTTP request details for tracking

        Args:
            endpoint (str): The endpoint the HTTP request was made to
            status (int): The response status code
            error (Exception): The HTTP request error
        """
        self.all_failed_requests.append({
                "endpoint": endpoint,
                "response_status": status,
                "error_type": f"{type(error).__name__}",
                "full_error": f"{error}",
            })
    
    def get_all_failed_requests(self) -> list[dict]:
        """Return dictionary of all failed requests

        Returns:
            dict: All failed requests from attempted HTTP requests
        """
        return self.all_failed_requests
    
    def _find_script_tags(self, response_html) -> list[str]:
        """Find all scripts tags in the HTTP response data

        Args:
            response_html (str): The HTML data from the HTTP request

        Returns:
            list[str]: A list of found script tags
        """
        response_html = response_html.lower()
        
        found_script_tags = []
        start = 0

        while True:
            start_index = response_html.find("<script>", start)

            if start_index == -1:
                break

            end_index = response_html.find("</script>", start_index)

            if end_index == -1:
                break

            end_index += len("</script>")

            script_tag = response_html[start_index:end_index]
            found_script_tags.append(script_tag)

            start = end_index
        
        return found_script_tags
      
    def _find_hyperlinks(self, response_html) -> list[str]:
        """Find all <a> tags in the HTTP response data

        Args:
            response_html (str): The HTML data from the HTTP request

        Returns:
            list[str]: A list of found <a> tags
        """
        response_html = response_html.lower()
        
        found_hyperlinks = []
        start = 0

        while True:
            start_index = response_html.find("<a ", start)

            if start_index == -1:
                break

            end_index = response_html.find("</a>", start_index)

            if end_index == -1:
                break

            end_index += len("</a>")

            hyperlink = response_html[start_index:end_index]
            found_hyperlinks.append(hyperlink)

            start = end_index

        return found_hyperlinks