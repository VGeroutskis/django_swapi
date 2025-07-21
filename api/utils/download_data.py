import requests


def fetch_swapi_data():
    # Disable SSL warnings for requests
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    )
    data = {}
    base_url = f"https://swapi.dev/api/"
    try:
        for entity in [
            "planets",
            "people",
            "films",
            "species",
            "vehicles",
            "starships",
        ]:
            data[entity] = []
            url = f"{base_url}{entity}"
            while url:
                print(f"Fetching data from: {url}")
                response = requests.get(url, verify=False)
                response.raise_for_status()
                data_chunk = response.json()
                data[entity].extend(data_chunk.get("results", []))
                url = data_chunk.get("next")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
