import random
from collections import namedtuple

import pytest
from django.db.models.base import ModelBase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

VIEWSET_IS_NONE = "View class is None."
URL_IS_NONE = "Url is None."
QUERYSET_IS_NONE = "Queryset is None."
MODEL_IS_NONE = "Model is None."

method = namedtuple("method", "shorthand action")
GET = method(shorthand="g", action={"get": "list"})
RETRIEVE = method(shorthand="r", action={"get": "retrieve"})
CREATE = method(shorthand="c", action={"post": "create"})
UPDATE = method(shorthand="u", action={"patch": "update"})
PARTIAL_UPDATE = method(shorthand="p", action={"patch": "partial_update"})
DELETE = method(shorthand="d", action={"delete": "destroy"})


@pytest.mark.django_db
class ModelViewSetTestBase(object):
    viewset = None
    factory = APIRequestFactory()
    url = None
    queryset = None
    model = None

    def run_common_assertions(self):
        if not self.viewset:
            raise AttributeError(VIEWSET_IS_NONE)
        if not self.url:
            raise AttributeError(URL_IS_NONE)
        if not self.queryset:
            raise AttributeError(QUERYSET_IS_NONE)
        if not self.model:
            raise AttributeError(MODEL_IS_NONE)

    def _run_unauthorized_assertion(self, request, view):
        response = view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def _authenticate_request(self, user, request, token=None):
        if token:
            force_authenticate(request, user, token=token)
        else:
            force_authenticate(request, user)

        return request

    def _run_base_view_assertion(self):
        pass

    def _run_cr_assertion(self, data):
        assert "valid_data" in data
        assert "invalid_data" in data

    def _get_factory_methods(self):
        return {
            "g": self.factory.get,
            "r": self.factory.get,
            "c": self.factory.post,
            "u": self.factory.patch,
            "p": self.factory.patch,
            "d": self.factory.delete
        }

    def run_assertions_for_get(self, user, token=None, keys=None):
        view = self.viewset.as_view(GET.action)
        request = self.factory.get(self.url)

        self._run_unauthorized_assertion(request, view)

        request = self._authenticate_request(user, request, token=token)
        response = view(request, test=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data
        assert len(response.data) == len(self.queryset)
        if keys:
            response_data_keys = response.data[0].keys()
            for key in keys:
                assert key in response_data_keys

    def run_assertions_for_retrieve(self, user, token=None, keys=None):
        view = self.viewset.as_view(RETRIEVE.action)
        request = self.factory.get(self.url)
        self._run_unauthorized_assertion(request, view)

        request = self._authenticate_request(user, request, token=token)

        request_data = random.choice(self.queryset)
        response = view(request, pk=request_data.pk, test=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data
        response_data = response.data
        if "id" in response_data:
            assert request_data.id == response_data["id"]
        if keys:
            for key in keys:
                print(key)
                assert key in response_data
                assert hasattr(request_data, key)
                try:
                    assert getattr(request_data, key) == response_data[key]
                except AssertionError:
                    value = getattr(request_data, key)
                    if isinstance(value, ModelBase):
                        assert value.pk == response_data[key]

    def run_assertions_for_partial_update(self, user, update_data, token=None):
        self._run_cr_assertion(update_data)

        view = self.viewset.as_view(PARTIAL_UPDATE.action)
        request = self.factory.patch(self.url)
        self._run_unauthorized_assertion(request, view)

        valid_data = update_data["valid_data"]
        invalid_data = update_data["invalid_data"]
        request = self.factory.patch(self.url, invalid_data)
        self._run_unauthorized_assertion(request, view)
        request = self.factory.patch(self.url, valid_data)
        self._run_unauthorized_assertion(request, view)

        request_data = random.choice(self.queryset)
        request = self._authenticate_request(user, request, token=token)
        response = view(request, pk=request_data.pk, test=True)
        assert response.status_code == status.HTTP_200_OK
        assert response.data
        response_data = response.data
        if "id" in response_data:
            assert response_data["id"] == request_data.id
        for key in valid_data.keys():
            assert key in response_data
            assert response_data[key] == valid_data[key]

        request = self.factory.patch(self.url, invalid_data)
        request = self._authenticate_request(user, request, token=token)
        response = view(request, pk=request_data.pk, test=True)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def run_assertions_for_create(self, user, create_data, token=None):
        self._run_cr_assertion(create_data)

        view = self.viewset.as_view(CREATE.action)
        request = self.factory.post(self.url)
        self._run_unauthorized_assertion(request, view)

        valid_data = create_data["valid_data"]
        invalid_data = create_data["invalid_data"]
        request = self.factory.post(self.url, invalid_data)
        self._run_unauthorized_assertion(request, view)
        request = self.factory.post(self.url, valid_data)
        self._run_unauthorized_assertion(request, view)

        request = self._authenticate_request(user, request, token=token)
        response = view(request, test=True)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data
        response_data = response.data
        for key in valid_data.keys():
            assert key in response_data
            assert response_data[key] == valid_data[key]

        request = self.factory.post(self.url, invalid_data)
        request = self._authenticate_request(user, request, token=token)
        response = view(request, test=True)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def run_assertions_for_destroy(self, user, token=None):
        view = self.viewset.as_view(DELETE.action)
        request = self.factory.delete(self.url)
        self._run_unauthorized_assertion(request, view)

        request = self._authenticate_request(user, request, token=token)
        request_data = random.choice(self.queryset)
        response = view(request, pk=request_data.pk, test=True)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = view(request, pk=request_data.pk, test=True)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        with pytest.raises(self.model.DoesNotExist):
            self.model.objects.get(pk=request_data.pk)

    def run_all_assertions(self, user, create_data, update_data, token=None, get_keys=None):
        self.run_common_assertions()
        self.run_assertions_for_get(user, keys=get_keys, token=token)
        self.run_assertions_for_create(user, create_data, token=token)
        self.run_assertions_for_retrieve(user, keys=get_keys, token=token)
        self.run_assertions_for_partial_update(user, update_data, token=token)
        self.run_assertions_for_destroy(user, token=token)

    def run_not_allowed_methods_assertions(self, user, not_allowed_methods, token=None):
        factory_methods = self._get_factory_methods()

        for method in not_allowed_methods:
            view = self.viewset.as_view(method.action)
            request = factory_methods[method.shorthand](self.url)
            self._run_unauthorized_assertion(request, view)

            request = self._authenticate_request(user, request, token=token)
            response = view(request)
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
