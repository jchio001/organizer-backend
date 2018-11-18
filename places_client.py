from http import HTTPStatus

import json
import os
import requests

google_places_nearby_url_template = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input=%s%s' \
                                    '&radius=5000&key=' + os.environ['FOOD_ORGANIZER_GOOGLE_API_KEY']


def get_places(query_string='a', location=None):
    places_response = requests.get(google_places_nearby_url_template
                                  % (query_string, f'&location={location}' if location else ""))

    places_response_json = json.loads(places_response.content)
    if places_response.status_code == HTTPStatus.OK and places_response_json.get('status') == "OK":
        return list(map(transform_places_dict, places_response_json.get('predictions'))), HTTPStatus.OK
    else:
        error_message = places_response_json.get('error_message')
        if error_message:
            return {'error': error_message}, HTTPStatus.INTERNAL_SERVER_ERROR
        else:
            return {'error': 'Google places API returned status %s' % places_response_json.get('status')}, \
                   HTTPStatus.INTERNAL_SERVER_ERROR


def transform_places_dict(places_dict):
    return {'place_id': places_dict.get('place_id'),
            'name': places_dict.get('description')}

