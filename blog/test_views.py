import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Post

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def another_user(db):
    return User.objects.create_user(username='anotheruser', password='anotherpassword')

@pytest.fixture
def post(db, user):
    return Post.objects.create(title='Test Post', content= 'Test Content', author = user)

#post_lists test
@pytest.mark.django_db
def test_get_all_posts(client, post):
    response = client.get(reverse('post_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_post_authenticated(client, user):
    client.force_authenticate(user=user)
    response = client.post(reverse('post_list'), {
        'title': 'New Post',
        'content': 'New Content',

    })
    assert response.status_code == 201
    assert response.data['title'] == 'New Post'

@pytest.mark.django_db
def test_create_post_unauthenticated(client):
    response = client.post(reverse('post_list'),{
        'title': 'New Post',
        'content': 'New Content',
    })
    assert response.status_code == 401

#Post details test
@pytest.mark.django_db
def test_get_single_post(client,post):
    response = client.get(reverse('post_detail', kwargs={'pk': post.pk}))
    assert response.status_code == 200
    assert response.data['title'] == 'Test Post'

@pytest.mark.django_db
def test_get_post_not_found(client):
    response = client.get(reverse('post_detail', kwargs={'pk': 999}))
    assert response.status_code == 404

@pytest.mark.django_db
def test_update_post_as_author(client, user, post):
    client.force_authenticate(user=user)
    response = client.put(reverse('post_detail', kwargs={'pk': post.pk}), {
        'title': 'Updated Title',
        'content': 'Updated Content',
    })
    assert response.status_code == 200
    assert response.data['title'] == 'Updated Title'

@pytest.mark.django_db
def test_update_post_as_wrong_user(client, another_user, post):
    client.force_authenticate(user=another_user)
    response = client.put(reverse('post_detail', kwargs={'pk': post.pk}), {
        'title': 'Hacked Title',
        'content': 'Hacked Content',
    })
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_post_as_author(client, user, post):
    client.force_authenticate(user=user)
    response = client.delete(reverse('post_detail', kwargs={'pk': post.pk}))
    assert response.status_code == 204

@pytest.mark.django_db
def test_delete_post_as_wrong_user(client, another_user, post):
    client.force_authenticate(user=another_user)
    response = client.delete(reverse('post_detail', kwargs={'pk': post.pk}))
    assert response.status_code  == 403