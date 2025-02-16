import time
import requests
from requests.exceptions import RequestException

def get_with_exponential_backoff(endpoint: str, headers: dict[str, str], timeout: int = 30) -> requests.Response:
    """
    Perform a GET request with exponential backoff retry logic

    This function sends a GET request to the specified endpoint with the provided headers.
    If the request fails, it will retry up to 5 times with exponential backoff.
    
    Parameters
    ----------
    endpoint : str
        The URL endpoint to send the GET request to
    headers : dict[str, str] 
        Headers to include in the request
    timeout : int, optional
        Request timeout in seconds, defaults to 30

    Returns
    -------
    requests.Response
        The response from the successful request

    Raises
    ------
    RequestException
        If all retries fail
    """
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            r = requests.get(endpoint, headers=headers, timeout=timeout)
            return r
        except RequestException as e:
            retry_count += 1
            if retry_count == max_retries:
                print(f"Max retries ({max_retries}) reached. Raising error.", flush=True)
                raise e
            # Calculate exponential backoff wait time: 2^retry_count seconds
            wait_time = 3 ** retry_count
            print(f"Request failed. Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})", flush=True)
            time.sleep(wait_time)
    
    # Add explicit return or raise to handle any unexpected cases
    raise RequestException("Request failed after all retries")