import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from v1.widget.constants import ONLY_ONE_EMBED_SCRIPT_ALLOWED, EMBED_DOES_NOT_EXIST
from v1.widget.models import Embed


@pytest.mark.integration
@pytest.mark.django_db
class TestWidgetViews:
    client = APIClient()
    url = '/api/v1/embed-widget/'

    def test_embed_all_actions_with_no_auth(self, embed_data):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.client.post(self.url, embed_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.client.patch(self.url, embed_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_embed_get_no_data(self, user):
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_embed_get_with_data(self, user, embed):
        self.client.force_authenticate(user)
        response = self.client.get(self.url)
        response_data = response.data
        assert response.status_code == status.HTTP_200_OK
        assert response_data['css'] == embed.css
        assert response_data['javascript'] == embed.javascript
        assert response_data["color"] == embed.color

    def test_embed_create_with_no_data(self, user, embed_data):
        self.client.force_authenticate(user)
        response = self.client.post(self.url, embed_data)
        response_data = response.data
        embed = Embed.objects.get()
        assert response.status_code == status.HTTP_201_CREATED
        assert response_data['css'] == embed.css
        assert response_data['javascript'] == embed.javascript
        assert response_data["color"] == embed.color

    def test_embed_create_with_data(self, user, embed):
        self.client.force_authenticate(user)
        response = self.client.post(self.url)
        response_data = response.data
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data['detail'] == ONLY_ONE_EMBED_SCRIPT_ALLOWED

    def test_embed_update_with_no_data(self, user, embed_data):
        self.client.force_authenticate(user)
        response = self.client.patch(self.url, embed_data)
        response_data = response.data
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response_data['detail'] == EMBED_DOES_NOT_EXIST

    def test_embed_update_with_data(self, user, embed):
        self.client.force_authenticate(user)
        data = {
            'company': user.company.id,
            'color': '#123456',
            'javascript': '<script></script>',
            'css': 'css'
        }
        response = self.client.patch(self.url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_embed_delete_with_data(self, user, embed):
        self.client.force_authenticate(user)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_embed_delete_with_no_data(self, user):
        self.client.force_authenticate(user)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
