import requests
import json
import time


TOKEN_FILE = '' # Type token file path
BUNDLE_URL = 'https://api.allegro.pl/sale/loyalty/promotions/'
BUNDLE_LIMIT = 1000


def get_token():
    with open(TOKEN_FILE, 'r') as file:
        token = file.readline()
    return token


def get_response(method, url, data=None):
    token = get_token()
    try:
        headers = {
            'Content-type': 'application/vnd.allegro.public.v1+json',
            'Accept': 'application/vnd.allegro.public.v1+json',
            'Authorization': 'Bearer ' + token
        }
        api_call_response = requests.request(method=method,
                                             url=url,
                                             headers=headers,
                                             params=data)
        api_call_response.raise_for_status()

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return api_call_response


def get_bundles(offer_id=None) -> dict:
    data = {
        'offer.id': offer_id,
        'limit': BUNDLE_LIMIT
    }
    bundles = get_response('GET', BUNDLE_URL, data)
    return json.loads(bundles.text)


def delete_bundle(id: str):
    json_object = get_response('DELETE', BUNDLE_URL + id)
    return json_object.status_code


def main(offer_id: str) -> None:
    bundles_data = get_bundles(offer_id)
    bundles = bundles_data.get('promotions', [])
    for bundle in bundles:
        print(delete_bundle(bundle['id']))
        time.sleep(1)


if __name__ == '__main__':
    main('') # Type offer id
