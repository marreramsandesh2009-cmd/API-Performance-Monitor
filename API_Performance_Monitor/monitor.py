import time
import requests
from urllib.parse import urlparse

def validate_url(url):
    parsed = urlparse(url)

    return parsed.scheme in ["http", "https"] and bool(parsed.netloc)

def check_api(url):
    if not validate_url(url):
        return {
            "url": url,
            "status": "Failed",
            "status_code": 0,
            "response_time": 0,
            "response_size": 0,
            "error": "Invalid URL. Use a complete HTTP or HTTPS URL."
        }

    start_time = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "API-Performance-Monitor/1.0"
            }
        )

        end_time = time.perf_counter()

        response_time = round((end_time - start_time) * 1000, 2)
        response_size = len(response.content)

        return {
            "url": url,
            "status": "Success" if response.ok else "Failed",
            "status_code": response.status_code,
            "response_time": response_time,
            "response_size": response_size,
            "error": ""
        }

    except requests.exceptions.Timeout:
        end_time = time.perf_counter()

        return {
            "url": url,
            "status": "Failed",
            "status_code": 408,
            "response_time": round((end_time - start_time) * 1000, 2),
            "response_size": 0,
            "error": "Request timed out."
        }

    except requests.exceptions.RequestException as error:
        end_time = time.perf_counter()

        return {
            "url": url,
            "status": "Failed",
            "status_code": 0,
            "response_time": round((end_time - start_time) * 1000, 2),
            "response_size": 0,
            "error": str(error)
        }