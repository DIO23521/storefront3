from store.models import Collection
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from model_bakery import baker


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection_data):
        return api_client.post('/store/collections/', collection_data)
    return do_create_collection

@pytest.fixture
def delete_collection(api_client):
    def do_delete_collection(collection_id):
        return api_client.delete(f'/store/collections/{collection_id}/')
    return do_delete_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):
        # AAA (Arrange, Act, Assert)
        #Arrange

        #Act
        client = APIClient()
        response = client.post('/store/collections/', { 'title': 'a' })

        #Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):
        #Arrange
        authenticate()

        #Act
        response = create_collection({ 'title': 'a' })

        #Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_data_is_invalid_returns_400(self, create_collection, authenticate):
        #Arrange
        authenticate(is_staff=True)

        #Act
        response = create_collection({ 'title': '' })

        #Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_if_data_is_valid_returns_201(self, create_collection, authenticate):
        #Arrange
        authenticate(is_staff=True)

        #Act
        response = create_collection({ 'title': 'a' })

        #Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestDeleteCollection:
    def test_if_user_is_not_admin_returns_403(self, authenticate, delete_collection):
        authenticate()
        collection = baker.make(Collection)
        
        response = delete_collection(collection.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_user_is_admin_returns_204(self, authenticate, delete_collection):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        
        response = delete_collection(collection.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT



@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)

        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }