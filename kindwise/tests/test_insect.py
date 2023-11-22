import base64
from datetime import datetime

import pytest
from kindwise.insect import InsectApi
from .conftest import IMAGE_DIR
from kindwise.models import Identification, Result, Input, Classification, Suggestion, SimilarImage


@pytest.fixture
def api(api_key):
    api_ = InsectApi(api_key=api_key)
    return api_


@pytest.fixture
def identification():
    return Identification(
        access_token='TDp7etcIfwK8LCh',
        model_version='insect_id:1.0.1',
        custom_id=None,
        input=Input(
            images=['https://insect.kindwise.com/media/images/2acb5cf7bd7a48b2afda07ef54f42e16.jpg'],
            datetime=datetime.fromisoformat('2023-11-22T08:49:26.136448+00:00'),
            latitude=None,
            longitude=None,
            similar_images=True,
        ),
        result=Result(
            classification=Classification(
                suggestions=[
                    Suggestion(
                        id='3a16a1c61de4d33b',
                        name='Osmia ' 'bicornis',
                        probability=0.9998153,
                        similar_images=[
                            SimilarImage(
                                id='08d93df0e7ecc5391d18be8e645a6baa',
                                url='https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/08d/93df0e7ecc5391d18be8e645a6baa.jpeg',
                                similarity=0.707,
                                url_small='https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/08d/93df0e7ecc5391d18be8e645a6baa.small.jpeg',
                                license_name='CC ' 'BY ' '4.0',
                                license_url='https://creativecommons.org/licenses/by/4.0/',
                                citation='Maarten ' 'Trekels',
                            ),
                            SimilarImage(
                                id='c9b945dda9d60950972250171bf31808',
                                url='https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/c9b/945dda9d60950972250171bf31808.jpeg',
                                similarity=0.698,
                                url_small='https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/c9b/945dda9d60950972250171bf31808.small.jpeg',
                                license_name='CC BY 4.0',
                                license_url='https://creativecommons.org/licenses/by/4.0/',
                                citation='John ' 'Forrester',
                            ),
                        ],
                        details={'entity_id': '3a16a1c61de4d33b', 'language': 'en'},
                    )
                ]
            )
        ),
        status='COMPLETED',
        sla_compliant_client=True,
        sla_compliant_system=True,
        created=datetime.fromtimestamp(1700642966.136448),
        completed=datetime.fromtimestamp(1700642966.580449),
    )


@pytest.fixture
def identification_dict():
    return {
        'access_token': 'TDp7etcIfwK8LCh',
        'completed': 1700642966.580449,
        'created': 1700642966.136448,
        'custom_id': None,
        'input': {
            'datetime': '2023-11-22T08:49:26.136448+00:00',
            'images': ['https://insect.kindwise.com/media/images/2acb5cf7bd7a48b2afda07ef54f42e16.jpg'],
            'latitude': None,
            'longitude': None,
            'similar_images': True,
        },
        'model_version': 'insect_id:1.0.1',
        'result': {
            'classification': {
                'suggestions': [
                    {
                        'details': {'entity_id': '3a16a1c61de4d33b', 'language': 'en'},
                        'id': '3a16a1c61de4d33b',
                        'name': 'Osmia bicornis',
                        'probability': 0.9998153,
                        'similar_images': [
                            {
                                'citation': 'Maarten ' 'Trekels',
                                'id': '08d93df0e7ecc5391d18be8e645a6baa',
                                'license_name': 'CC ' 'BY ' '4.0',
                                'license_url': 'https://creativecommons.org/licenses/by/4.0/',
                                'similarity': 0.707,
                                'url': 'https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/08d/93df0e7ecc5391d18be8e645a6baa.jpeg',
                                'url_small': 'https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/08d/93df0e7ecc5391d18be8e645a6baa.small.jpeg',
                            },
                            {
                                'citation': 'John ' 'Forrester',
                                'id': 'c9b945dda9d60950972250171bf31808',
                                'license_name': 'CC ' 'BY ' '4.0',
                                'license_url': 'https://creativecommons.org/licenses/by/4.0/',
                                'similarity': 0.698,
                                'url': 'https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/c9b/945dda9d60950972250171bf31808.jpeg',
                                'url_small': 'https://insect-id.ams3.cdn.digitaloceanspaces.com/similar_images/1/c9b/945dda9d60950972250171bf31808.small.jpeg',
                            },
                        ],
                    }
                ]
            }
        },
        'sla_compliant_client': True,
        'sla_compliant_system': True,
        'status': 'COMPLETED',
    }


@pytest.fixture
def image_path():
    return IMAGE_DIR / 'bee.jpeg'


@pytest.fixture
def image_base64(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode("ascii")


def test_identify(api, api_key, identification, identification_dict, image_path, image_base64, requests_mock):
    requests_mock.post(
        f'{api.identify_url}',
        json=identification_dict,
    )
    response_identification = api.identify(image_path)
    assert len(requests_mock.request_history) == 1
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.identify_url}'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert request_record.json() == {'images': [image_base64], 'similar_images': True}
    assert response_identification == identification

    response_identification = api.identify(image_path, as_dict=True)
    request_record = requests_mock.request_history.pop()
    assert response_identification == identification_dict

    response_identification = api.identify(
        image_path, similar_images=False, details=['image'], language='cz', latitude_longitude=(1.0, 2.0)
    )
    assert len(requests_mock.request_history) == 1
    request_record = requests_mock.request_history.pop()
    assert request_record.method == 'POST'
    assert request_record.url == f'{api.identify_url}?details=image&language=cz'
    assert request_record.headers['Content-Type'] == 'application/json'
    assert request_record.headers['Api-Key'] == api_key
    assert request_record.json() == {
        'images': [image_base64],
        'similar_images': False,
        'latitude': 1.0,
        'longitude': 2.0,
    }