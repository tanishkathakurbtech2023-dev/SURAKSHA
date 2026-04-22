import os
import tempfile

from fastapi.testclient import TestClient

_db_file = tempfile.NamedTemporaryFile(delete=False)
os.environ['SQLITE_DB_PATH'] = _db_file.name
os.environ['SURAKSHA_API_KEY'] = 'test-api-key'

from backend.main import app  # noqa: E402


client = TestClient(app)
HEADERS = {'X-API-Key': 'test-api-key'}


def test_health_and_risk() -> None:
    health = client.get('/health')
    assert health.status_code == 200
    assert health.json()['status'] == 'ok'

    response = client.post(
        '/api/auth/risk',
        headers=HEADERS,
        json={
            'user_id': 'u1',
            'amount': 1200,
            'device_trust': 0.9,
            'network_risk': 0.1,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body['level'] in {'low', 'medium', 'high'}
    assert body['challenge']

    behaviour = client.post('/api/auth/behaviour', headers=HEADERS, json={'session_features': [0.3, 0.4, 0.55, 0.6]})
    assert behaviour.status_code == 200
    assert 'trust_score' in behaviour.json()


def test_transaction_flow_admin_and_agents() -> None:
    tx = client.post(
        '/api/transactions/process',
        headers=HEADERS,
        json={
            'user_id': 'u2',
            'txn_id': 'txn-001',
            'to_account': 'ACC12345',
            'amount': 1000,
            'device_trust': 0.8,
            'network_risk': 0.2,
            'nonce': 'nonce-12345678',
        },
    )
    assert tx.status_code == 200
    data = tx.json()
    assert data['decision'] in {'allow', 'flag', 'block'}
    assert data['signature']
    assert len(data['audit_hash']) == 64
    assert data['recommended_action']
    assert data['education_tip']

    summary = client.get('/api/admin/summary', headers=HEADERS)
    assert summary.status_code == 200

    report = client.get('/api/admin/report', headers=HEADERS)
    assert report.status_code == 200
    assert 'report' in report.json()

    audit_query = client.post('/api/admin/audit/query', headers=HEADERS, json={'query': 'txn_id'})
    assert audit_query.status_code == 200
    assert 'count' in audit_query.json()

    helpdesk = client.post('/api/helpdesk/chat', headers=HEADERS, json={'message': 'should i share otp?', 'language': 'en'})
    assert helpdesk.status_code == 200
    assert helpdesk.json()['intent'] == 'phishing_warning'
    assert 'entities' in helpdesk.json()
    assert 'incident_category' in helpdesk.json()


def test_nonce_and_auth_guard() -> None:
    first = client.post(
        '/api/transactions/process',
        headers=HEADERS,
        json={
            'user_id': 'u3',
            'txn_id': 'txn-101',
            'to_account': 'ACC12345',
            'amount': 1000,
            'device_trust': 0.8,
            'network_risk': 0.2,
            'nonce': 'nonce-replay-1',
        },
    )
    assert first.status_code == 200

    duplicate = client.post(
        '/api/transactions/process',
        headers=HEADERS,
        json={
            'user_id': 'u3',
            'txn_id': 'txn-102',
            'to_account': 'ACC12345',
            'amount': 1000,
            'device_trust': 0.8,
            'network_risk': 0.2,
            'nonce': 'nonce-replay-1',
        },
    )
    assert duplicate.status_code == 409

    blocked = client.get('/api/admin/summary')
    assert blocked.status_code == 401
