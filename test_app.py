import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test the homepage."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert 'Welcome to Zumo!' in data
    assert "Gabriel's Zumo Tech Assignment" in data


def test_kubernetes_info(client, mocker):
    """Test the /api/kubernetes-info route."""
    mocked_info = {
        'pod_name': 'test_pod',
        'pod_ip': '127.0.0.1',
        'namespace': 'test_namespace',
        'kubernetes_api': 'test_api'
    }
    mocker.patch('app.get_kubernetes_info', return_value=mocked_info)
    response = client.get('/api/kubernetes-info')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == mocked_info

def test_dynamic_message(client):
    """Test the /api/message route."""
    response = client.get('/api/message')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'Hello from Kubernetes!' in json_data['message']

def test_server_info(client):
    """Test the /api/server-info route."""
    response = client.get('/api/server-info')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'hostname' in json_data
    assert 'ip' in json_data