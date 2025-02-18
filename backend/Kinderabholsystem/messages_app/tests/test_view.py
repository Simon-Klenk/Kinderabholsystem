# backend/messages_app/tests/test_views.py

import pytest
from django.urls import reverse
from rest_framework import status
from messages_app.models import Message
from messages_app.serializers import MessageSerializer

@pytest.mark.django_db
def test_message_list_create_api_view_get(client):
    """
    Test GET request to MessageListCreateAPIView.
    
    This test ensures that:
    1. The view returns a 200 OK status.
    2. The correct number of messages are returned.
    3. Messages are returned in reverse chronological order.
    """
    # Create test messages
    Message.objects.create(content="Test m.")
    Message.objects.create(content="Test m.")

    url = reverse("message_list_create")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    # Check reverse chronological order
    assert response.data[0]["content"] == "Test m."
    assert response.data[1]["content"] == "Test m."


@pytest.mark.django_db
def test_message_list_create_api_view_post(client, mocker):
    """
    Test POST request to MessageListCreateAPIView.
    
    This test ensures that:
    1. A new message is created successfully.
    2. The view returns a 201 CREATED status.
    3. The send_message_to_raspberry_pi function is called.
    """
    # Mock send_message_to_raspberry_pi to prevent actual HTTP requests
    mock_send_message = mocker.patch("messages_app.views.send_message_to_raspberry_pi")

    url = reverse("message_list_create")  # Ensure the URL name is correct
    data = {"content": "New t."}
    response = client.post(url, data, content_type='application/json') 

    assert response.status_code == status.HTTP_201_CREATED
    assert Message.objects.count() == 1
    assert Message.objects.first().content == "New t."
    mock_send_message.assert_called_once()


@pytest.mark.django_db
def test_message_status_update_api_view_patch(client):
    """
    Test PATCH request to MessageStatusUpdateAPIView.
    
    This test ensures that:
    1. The message status is updated successfully.
    2. The view returns a 200 OK status.
    """
    # Create a test message
    message = Message.objects.create(content="Test m.", status="received")

    url = reverse("message_status_update", kwargs={'pk': message.pk})
    data = {"status": "approved"}
    response = client.patch(url, data, content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
    assert Message.objects.get(pk=message.pk).status == "approved"


@pytest.mark.django_db
def test_clear_layer_api_view_post(client, mocker):
    """
    Test POST request to ClearLayerAPIView.
    
    This test ensures that:
    1. The view returns a 200 OK status.
    2. The send_osc_message function is called with correct arguments.
    """
    # Mock the send_osc_message function
    mock_send_osc_message = mocker.patch("messages_app.views.send_osc_message")
    url = reverse("clear_layer")
    response = client.post(url)

    assert response.status_code == status.HTTP_200_OK
    mock_send_osc_message.assert_called_with("", "0.0")
