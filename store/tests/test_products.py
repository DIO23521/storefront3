from store.models import Product
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from model_bakery import baker


@pytest.fixture
def create_product(api_client):
    def do_create_product(product_data):
        return api_client.post('/store/products/', product_data)
    return do_create_product



@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, create_product):

        response = create_product({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_product):
        authenticate()

        response = create_product({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

