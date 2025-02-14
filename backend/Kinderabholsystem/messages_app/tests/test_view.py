# backend/messages_app/tests/test_views.py  (Stelle sicher, dass der Pfad stimmt!)

import pytest
from django.urls import reverse
from rest_framework import status
from messages_app.models import Message  # Stelle sicher, dass der App-Name stimmt!
from messages_app.serializers import MessageSerializer  # Stelle sicher, dass der App-Name stimmt!

@pytest.mark.django_db
def test_message_list_create_api_view_get(client):
    """Test GET request to MessageListCreateAPIView."""
    # Erstelle ein paar Test-Nachrichten
    Message.objects.create(content="Test message 1")
    Message.objects.create(content="Test message 2")

    url = reverse("message_list_create")  # Stelle sicher, dass der URL-Name stimmt!
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    # Überprüfe die umgekehrte chronologische Reihenfolge
    assert response.data[0]["content"] == "Test message 2"
    assert response.data[1]["content"] == "Test message 1"


@pytest.mark.django_db
def test_message_list_create_api_view_post(client, mocker):
    """Test POST request to MessageListCreateAPIView."""
    # Mock send_message_to_raspberry_pi, um tatsächliche HTTP-Requests zu verhindern
    mock_send_message = mocker.patch("messages_app.views.send_message_to_raspberry_pi")  # Stelle sicher, dass der App-Name stimmt!

    url = reverse("message_list_create")  # Stelle sicher, dass der URL-Name stimmt!
    data = {"content": "Neue Test-Nachricht"}
    response = client.post(url, data, content_type='application/json')  # Content-Type ist wichtig!

    assert response.status_code == status.HTTP_201_CREATED
    assert Message.objects.count() == 1
    assert Message.objects.first().content == "Neue Test-Nachricht"
    mock_send_message.assert_called_once()  # Überprüfe, ob die Mock-Funktion aufgerufen wurde


@pytest.mark.django_db
def test_message_status_update_api_view_patch(client):
    """Test PATCH request to MessageStatusUpdateAPIView."""

    # Erstelle eine Test-Nachricht
    message = Message.objects.create(content="Test message", status="received")

    url = reverse("message_status_update", kwargs={'pk': message.pk})  # Stelle sicher, dass der URL-Name stimmt!
    data = {"status": "approved"}
    response = client.patch(url, data, content_type='application/json')  # Content-Type ist wichtig!

    assert response.status_code == status.HTTP_200_OK
    assert Message.objects.get(pk=message.pk).status == "approved"


@pytest.mark.django_db
def test_clear_layer_api_view_post(client, mocker):
    """Test POST request to ClearLayerAPIView."""
    # Moche die send_osc_message Funktion
    mock_send_osc_message = mocker.patch("messages_app.views.send_osc_message")  # Stelle sicher, dass der App-Name stimmt!
    url = reverse("clear_layer")  # Stelle sicher, dass der URL-Name stimmt!
    response = client.post(url)

    assert response.status_code == status.HTTP_200_OK
    mock_send_osc_message.assert_called_with("", "0.0") #Überprüfe, ob die Funktion mit den korrekten Argumenten aufgerufen wurde
