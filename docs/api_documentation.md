Django API Documentation: Message Management with OSC Integration and Raspberry Pi Communication

Overview

This API provides functionality to manage messages with integration to Resolume Arena (via OSC communication) and Raspberry Pi. The system allows sending messages to Resolume Arena's text clips, controlling their opacity, and displaying or clearing them dynamically. Messages are also forwarded to a Raspberry Pi endpoint for further processing.

Table of Contents

API Endpoints 1.1. GET /messages/ 1.2. POST /messages/ 1.3. PATCH /messages/{pk}/ 1.4. POST /clear/
Models and Serializers
Helper Functions
OSC Communication Details
API Endpoints


1.1 GET /messages/
Retrieve the last 5 messages from the database, ordered by creation time.

Response

200 OK: A list of the most recent 5 messages.
Example:

[
  {
    "id": 1,
    "content": "Parents of students, please check in.",
    "status": "approved",
    "created_at": "2025-02-14T10:00:00Z"
  },
  ...
]


1.2 POST /messages/
Create a new message and forward it to the Raspberry Pi.

Request Body

content: The message text content to be displayed.
Response

201 Created: Message successfully created and forwarded to Raspberry Pi.
400 Bad Request: Invalid data provided.
Example:

{
  "content": "Urgent: Please visit the check-in desk."
}
Response:

{
  "id": 1,
  "content": "Urgent: Please visit the check-in desk.",
  "status": "created",
  "created_at": "2025-02-14T10:05:00Z"
}


1.3 PATCH /messages/{pk}/
Update the status of a message. The possible statuses are received, approved, and displayed.

Request Body

status: The new status of the message.
Response

200 OK: Status updated successfully.
400 Bad Request: Invalid status value.
404 Not Found: Message not found.
Example:

{
  "status": "approved"
}
Response:

{
  "id": 1,
  "content": "Urgent: Please visit the check-in desk.",
  "status": "approved",
  "created_at": "2025-02-14T10:05:00Z"
}


1.4 POST /clear/
Clear the current message display in Resolume Arena and stop any active display threads.

Response

200 OK: Display cleared successfully.
Models and Serializers

Message Model:
id: Integer, Primary Key.
content: CharField, the message content.
status: CharField, represents the message status (e.g., created, approved, displayed, received).
created_at: DateTimeField, the timestamp when the message was created.
MessageSerializer: Serializes the Message model into JSON format for API interaction.
Helper Functions

send_osc_message(message: str, opacity: float)
Sends an OSC message to Resolume Arena to control text display and layer opacity.

Args:
message: The message text to display on the Resolume clips.
opacity: The opacity value for the layer (between 0.0 and 1.0).
delayed_send_osc_message(message: str, delay: int, message_pk: int)
Manages the delayed display of a message, using a thread to clear the message after a certain duration.

Args:
message: The message to display.
delay: The delay in seconds before clearing the message.
message_pk: The primary key of the message object.
send_message_to_raspberry_pi(content: str, pk: int)
Forwards the message content to the Raspberry Pi endpoint for further handling.

Args:
content: The message text to send.
pk: The primary key of the message object.
update_state(pk: int, new_status: str)
Updates the status of the message and triggers OSC communication if the status is approved.

Args:
pk: The primary key of the message object.
new_status: The new status to assign to the message (received, approved, displayed).
OSC Communication

Resolume IP: 192.168.1.109 (IP address of the Resolume software)
Resolume Port: 7000 (default OSC port)
OSC Paths:
PARAM_PATH_OPACITY: /composition/layers/4/video/opacity (controls the opacity of layer 4 in Resolume)
PARAM_PATH_TEMPLATE: /composition/layers/4/clips/{clip_id}/video/effects/textblock/effect/text/params/lines (controls the text for 20 clips in layer 4)
URL Configuration

from django.urls import path
from .views import MessageListCreateAPIView, MessageStatusUpdateAPIView, ClearLayerAPIView

urlpatterns = [
    path('messages/', MessageListCreateAPIView.as_view(), name='message_list_create'),
    path('messages/<int:pk>/', MessageStatusUpdateAPIView.as_view(), name='message_status_update'),
    path('clear/', ClearLayerAPIView.as_view(), name='clear_layer'),
]