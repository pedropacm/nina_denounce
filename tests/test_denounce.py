import io

from mock import call, MagicMock, mock_open
import falcon
from falcon import testing
import json
import pytest

from nina_denounce.util.crypto import encode_rs512
from nina_denounce.repo.denounce_repo import DenounceRepo, Denounce
import nina_denounce.app
import nina_denounce.denounce


@pytest.fixture
def client():
    api = nina_denounce.app.create_app()
    return testing.TestClient(api)


# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_post_denounce_with_right_input(client):
    denounce_payload = {
        "lat": "3.7255483",
        "lon": "-38.5280283",
        "bus_number": "12345"
    }
    response = client.simulate_post(
        '/api/v1/denounce/create',
        body = json.dumps(denounce_payload, ensure_ascii=False),
        headers={'content-type': falcon.MEDIA_JSON}
    )

    expected_response_body = {
        "status": "OK",
        "denounce_id": "1"
    }
    assert response.status == falcon.HTTP_OK
    assert response.json == expected_response_body

def test_post_denounce_missing_input_values(client):
    denounce_payload = {
        "lat": "3.7255483",
        "bus_number": "12345"
    }
    response = client.simulate_post(
        '/api/v1/denounce/create',
        body = json.dumps(denounce_payload, ensure_ascii=False),
        headers={'content-type': falcon.MEDIA_JSON}
    )

    expected_response_body = {
        "status": "Bad Request"
    }
    assert response.status == falcon.HTTP_BAD_REQUEST
    assert response.json == expected_response_body

def test_complete_denounce_success(client):
    denounce_payload = {
        "denounce_id": "1",
        "description": "Homem gritou comigo no onibus."
    }
    token = encode_rs512({'user_id': 3})
    response = client.simulate_put(
        '/api/v1/denounce/complete',
        body = json.dumps(denounce_payload, ensure_ascii=False),
        headers={
            'content-type': falcon.MEDIA_JSON,
            'Authorization': 'Bearer ' + token
        }
    )

    expected_response_body = {
        "status": "OK",
        "denounce_id": "1"
    }
    assert response.status == falcon.HTTP_OK
    assert response.json == expected_response_body

    denounce_repo = DenounceRepo()
    saved_denounce = denounce_repo.find_by_id(1)

    assert saved_denounce.user_id == 3
    assert saved_denounce.description == denounce_payload['description']

def test_complete_denounce_bad_header(client):
    denounce_payload = {
        "denounce_id": "1",
        "description": "Homem gritou comigo no onibus."
    }
    token = "Bad token"
    response = client.simulate_put(
        '/api/v1/denounce/complete',
        body = json.dumps(denounce_payload, ensure_ascii=False),
        headers={
            'content-type': falcon.MEDIA_JSON,
            'Authorization': 'Bearer ' + token
        }
    )

    expected_response_body = {
        "status": "Bad Request"
    }
    assert response.status == falcon.HTTP_BAD_REQUEST
    assert response.json == expected_response_body