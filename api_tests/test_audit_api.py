
import pytest

class TestAuditActionItems:

    def test_get_all_audit_items_returns_200(self, session, base_url):
        response = session.get(f"{base_url}/todos")
        assert response.status_code == 200

    def test_audit_items_contain_required_fields(self, session, base_url):
        response = session.get(f"{base_url}/todos/1")
        data = response.json()
        for field in ["id", "title", "completed", "userId"]:
            assert field in data

    def test_get_nonexistent_audit_item_returns_404(self, session, base_url):
        response = session.get(f"{base_url}/todos/99999")
        assert response.status_code == 404

    def test_filter_open_audit_items(self, session, base_url):
        response = session.get(f"{base_url}/todos", params={"completed": "false"})
        data = response.json()
        assert isinstance(data, list)
        assert all(item["completed"] is False for item in data)

    def test_filter_closed_audit_items(self, session, base_url):
        response = session.get(f"{base_url}/todos", params={"completed": "true"})
        data = response.json()
        assert isinstance(data, list)
        assert all(item["completed"] is True for item in data)


class TestAuditActionItemCreation:

    def test_create_audit_item_returns_201(self, session, base_url, valid_audit_item_payload):
        response = session.post(f"{base_url}/todos", json=valid_audit_item_payload)
        assert response.status_code == 201

    def test_new_audit_item_is_open_by_default(self, session, base_url, valid_audit_item_payload):
        response = session.post(f"{base_url}/todos", json=valid_audit_item_payload)
        data = response.json()
        assert data["completed"] is False

    def test_create_audit_item_returns_assigned_id(self, session, base_url, valid_audit_item_payload):
        response = session.post(f"{base_url}/todos", json=valid_audit_item_payload)
        data = response.json()
        assert "id" in data
        assert isinstance(data["id"], int)