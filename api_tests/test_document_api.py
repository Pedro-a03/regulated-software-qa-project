import pytest

class TestUserManagement:

    def test_get_all_users_returns_200(self, session, base_url):
        response = session.get(f"{base_url}/users")
        assert response.status_code == 200

    def test_users_list_is_not_empty(self, session, base_url):
        response = session.get(f"{base_url}/users")
        data = response.json()
        assert len(data) > 0

    def test_user_record_has_required_fields(self, session, base_url):
        response = session.get(f"{base_url}/users/1")
        data = response.json()
        for field in ["id", "name", "username", "email"]:
            assert field in data

    def test_get_nonexistent_user_returns_404(self, session, base_url):
        response = session.get(f"{base_url}/users/99999")
        assert response.status_code == 404

    def test_user_email_format_is_valid(self, session, base_url):
        response = session.get(f"{base_url}/users")
        users = response.json()
        for user in users:
            assert "@" in user["email"]

    def test_get_documents_owned_by_user(self, session, base_url):
        response = session.get(f"{base_url}/posts", params={"userId": 1})
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert all(doc["userId"] == 1 for doc in data)
