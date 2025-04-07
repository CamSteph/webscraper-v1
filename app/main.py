# main.py

from helpers.handle_requests import HandleBatchRequests
from helpers.store_data import StoreBatchData
# import json
# json.dumps(data, indent=4)

# __HIGHLIGHT_COLOR: str = "\033[92m"
    # __ENDC: str = "\033[0m"
    # print(f"{self.__HIGHLIGHT_COLOR}Status:{self.__ENDC} " + str(response.status_code))
    # print(f"{self.__HIGHLIGHT_COLOR}Encoding:{self.__ENDC} " + response.encoding)
    # print(f"{self.__HIGHLIGHT_COLOR}Headers:{self.__ENDC} " + str(response.headers))


def generate_message() -> None:
    """Display the welcome message to the user
    """
    print("Welcome to WebScraper v1!")
    print("Created by: Cameron Stephenson")

def validate_url(endpoint : str) -> bool:
    """Return true if the url endpoint is of valid format, false otherwise.

    Args:
        endpoint (str): The URL endpoint

    Returns:
        bool: True if url endpoint is valid format, otherwise false
    """
    if endpoint == "done":
        return True
    if not endpoint:
        return False
    if len(endpoint) < 4:
        return False
    if "." not in endpoint:
        return False
    if endpoint.startswith(".") or endpoint.endswith("."):
        return False
    return True

def retrieve_url() -> str:
    while True:
        endpoint = input("Enter an endpoint (or 'done' to finish): ").lower()
        if validate_url(endpoint):
            return endpoint
        else:
            print("Invalid URL - please try again")

if __name__ == "__main__":
    generate_message()
    batch: HandleBatchRequests = HandleBatchRequests()

    while True:
        endpoint = retrieve_url()
        if endpoint == "done":
            break
        elif endpoint:
            batch.set_url_endpoint(endpoint)
        else:
            break

    for endpoint in batch.get_all_url_endpoints():
        batch.make_standard_get_request(endpoint)

    response_data = batch.get_all_response_data()
    failed_requests = batch.get_all_failed_requests()

    if response_data:
        cached_data = StoreBatchData(response_data)
        cached_data.write_to_current_cache()
        cached_data.append_to_history_cache()
        cached_data.get_current_cache()

    if failed_requests:
        print("Failed Requests: ")
        for fail in failed_requests:
            print(f"\033[31m{fail['full_error']}\033[0m")