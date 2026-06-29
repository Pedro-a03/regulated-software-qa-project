import pytest


class TestCAPARetrieval:

    def test_get_all_capa_records_returns_200(self, session, base_url):
        response = session.get(f"{base_url}/posts")
        assert response.status_code == 200

    def test_get_all_capa_records_returns_list(self, session, base_url):
        response = session.get(f"{base_url}/posts")
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_single_capa_record_returns_200(self, session, base_url):
        response = session.get(f"{base_url}/posts/1")
        assert response.status_code == 200

    def test_get_single_capa_record_has_required_fields(self, session, base_url):
        response = session.get(f"{base_url}/posts/1")
        data = response.json()
        for field in ["id", "title", "body", "userId"]:
            assert field in data

    def test_get_nonexistent_capa_record_returns_404(self, session, base_url):
        response = session.get(f"{base_url}/posts/99999")
        assert response.status_code == 404

    def test_capa_records_filtered_by_user(self, session, base_url):
        response = session.get(f"{base_url}/posts", params={"userId": 1})
        data = response.json()
        assert all(record["userId"] == 1 for record in data)


class TestCAPACreation:

    def test_create_capa_record_returns_201(self, session, base_url, valid_capa_payload):
        response = session.post(f"{base_url}/posts", json=valid_capa_payload)
        assert response.status_code == 201

    def test_create_capa_record_returns_id(self, session, base_url, valid_capa_payload):
        response = session.post(f"{base_url}/posts", json=valid_capa_payload)
        data = response.json()
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_capa_record_persists_title(self, session, base_url, valid_capa_payload):
        response = session.post(f"{base_url}/posts", json=valid_capa_payload)
        data = response.json()
        assert data["title"] == valid_capa_payload["title"]


class TestCAPAUpdate:

    def test_update_capa_record_returns_200(self, session, base_url, valid_capa_payload):
        updated = {**valid_capa_payload, "title": "CAPA-2026-001: CLOSED"}
        response = session.put(f"{base_url}/posts/1", json=updated)
        assert response.status_code == 200

    def test_update_capa_record_reflects_changes(self, session, base_url, valid_capa_payload):
        new_title = "CAPA-2026-001: CLOSED"
        updated = {**valid_capa_payload, "title": new_title}
        response = session.put(f"{base_url}/posts/1", json=updated)
        data = response.json()
        assert data["title"] == new_title