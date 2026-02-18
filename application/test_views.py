import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Notes
# Create your tests here.
@pytest.fixture
def client(db):
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='name', password='password')

@pytest.fixture
def another_user(db):
    return User.objects.create_user(username='another name', password='another password')

@pytest.fixture
def notes(db, user):
    return Notes.objects.create(title='test post', content='test content', author=user )

 ### NOTES_VIEW FUNCTION ###
@pytest.mark.django_db
def test_get_all_notes(client):
    response = client.get(reverse('notes_view'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_notes_authenticated(client, user):
    client.force_authenticate(user=user)
    response = client.post(reverse('notes_view'),{
        'title': 'new title',
        'content': 'new content',
    })
    assert response.status_code == 201
    assert response.data['title'] == 'new title'

@pytest.mark.django_db
def test_post_notes_not_authenticated(client):
    response = client.post(reverse('notes_view'), {
        'title': 'new title',
        'content': 'new content'
    })
    assert response.status_code == 401

### NOTE DETAIL FUNCTION ###
@pytest.mark.django_db
def test_note_not_found(client, user, notes):
    client.force_authenticate(user=user)
    response = client.get(reverse('notes_detail_view', kwargs={'pk': 999}))
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_note_as_author(client, user, notes):
    client.force_authenticate(user=user)
    response = client.get(reverse('notes_detail_view', kwargs={'pk': notes.pk}))
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_note_unauthenticated(client, notes):
    response = client.get(reverse('notes_detail_view', kwargs={'pk': notes.pk}))
    assert response.status_code == 401

@pytest.mark.django_db
def test_get_note_wrong_user(client, another_user, notes):
    client.force_authenticate(user=another_user)
    response = client.get(reverse('notes_detail_view', kwargs={'pk': notes.pk}))
    assert response.status_code == 403

@pytest.mark.django_db
def test_update_note_as_author(client, notes, user):
    client.force_authenticate(user=user)
    response = client.put(reverse('notes_detail_view', kwargs={'pk': notes.pk}), {
        'title': 'updated title',
        'content': 'updated content'
    })
    assert response.status_code == 200
    assert response.data['title'] == 'updated title'

@pytest.mark.django_db
def test_update_note_as_wrong_user(client, another_user, notes):
    client.force_authenticate(user=another_user)
    response = client.put(reverse('notes_detail_view', kwargs={'pk': notes.pk}), {
        'title': 'hacked Title',
        'content': 'hacked content'
    })
    assert response.status_code == 403

@pytest.mark.django_db
def test_update_note_unauthenticated(client, notes):
    response = client.put(reverse('notes_detail_view', kwargs={'pk': notes.pk}),{
        'title': 'updated title',
        'content': 'updated content'
    })
    assert response.status_code == 401

@pytest.mark.django_db
def test_delete_as_author(client, notes, user):
    client.force_authenticate(user=user)
    response = client.delete(reverse('notes_detail_view', kwargs={'pk': notes.pk}))
    assert response.status_code == 204

@pytest.mark.django_db
def test_delete_not_as_author(client, notes, another_user):
    client.force_authenticate(user=another_user)
    response = client.delete(reverse('notes_detail_view', kwargs={'pk': notes.pk}))
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_unauthenticated(client, notes):
    response = client.delete(reverse('notes_detail_view', kwargs={'pk': notes.pk}))
    assert response.status_code == 401







