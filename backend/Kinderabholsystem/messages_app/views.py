"""
Django View Module for Message Management with OSC Integration and Raspberry Pi Communication
"""

import threading
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from pythonosc.udp_client import SimpleUDPClient
import requests
import logging

# OSC Configuration for Resolume Arena
RESOLUME_IP = "192.168.104.10"  # Resolume software IP address
RESOLUME_PORT = 7000            # Default OSC port in Resolume
client = SimpleUDPClient(RESOLUME_IP, RESOLUME_PORT)

# Resolume OSC parameter paths
PARAM_PATH_OPACITY = "/composition/layers/6/video/opacity"
PARAM_PATH = "/composition/layers/6/clips/1/video/effects/textblock/effect/text/params/lines"

# Global thread controller for message display management
active_thread = None
stop_event = threading.Event()
clear_requested = False  # Flag for manual clear operations
number = 0
logger = logging.getLogger(__name__)

def send_osc_message(message: str, opacity: float) -> None:
    """
    Send OSC message to Resolume Arena to control text display.
    
    Args:
        message (str): Text content to display
        opacity (float): Layer opacity (0.0-1.0)
        
    Sends message to all 20 text clips in layer 4 and controls layer opacity.
    """
    try:
        opacity = float(opacity)
        client.send_message(PARAM_PATH, message)
        client.send_message(PARAM_PATH_OPACITY, opacity)
        print(f"Sent OSC message: {message}")
    except Exception as e:
        print(f"OSC communication error: {e}")


def delayed_send_osc_message(message: str, delay: int = 120, message_pk: int = None) -> None:
    """
    Manage delayed message clearing with thread control.
    
    Args:
        message (str): Content to display
        delay (int): Display duration in seconds
        message_pk (int): Primary key of Message object
        
    Immediately shows message, then clears it after delay unless interrupted.
    """
    global active_thread, stop_event, number
    
    # Stop any existing message thread
    if active_thread and active_thread.is_alive():
        stop_event.set()
        active_thread.join()
        stop_event.clear()

    # Show initial message
    if "Medizinischer Notfall:" in message:
        logger.debug(message)
        send_osc_message(message, "1.0")
    else:
        send_osc_message(f"Die Eltern von {message} bitte zum Check-in kommen", "1.0")
    number = message_pk

    def send_after_delay():
        """Thread target function for delayed operations"""
        start = time.time()
        while (time.time() - start) < delay:
            if stop_event.is_set():
                print("Message display interrupted by new message")
                return
            time.sleep(0.1)  # Allow for interrupt checks
            
        # Clear message after delay
        send_osc_message("", "0.0")
        
        # Update message status if PK provided
        if message_pk:
            update_state(message_pk, "displayed")
            print(f"Updated message {message_pk} to 'displayed' status")

    # Start new display thread
    active_thread = threading.Thread(target=send_after_delay)
    active_thread.start()


def send_message_to_raspberry_pi(content: str, pk: int) -> None:
    """
    Forward messages to Raspberry Pi endpoint.
    
    Args:
        content (str): Message text content
        pk (int): Primary key of Message object
    """
    RASPBERRY_PI_URL = "http://192.168.104.212/"
    
    try:
        response = requests.post(
            RASPBERRY_PI_URL,
            json={"id": pk, "message": content}
        )
        
        if response.status_code == 200:
            print("Message successfully forwarded to Raspberry Pi")
            update_state(pk, "received")
        else:
            print(f"RPi communication error: {response.status_code}")
    except Exception as e:
        print(f"RPi connection failed: {e}")


def update_state(pk: int, new_status: str) -> bool:
    """
    Update message status and trigger OSC communication when approved.
    
    Args:
        pk (int): Primary key of Message object
        new_status (str): New status value
        
    Returns:
        bool: True if update successful, False otherwise
        
    Triggers OSC display when status changes to 'approved'
    """
    try:
        message = Message.objects.get(pk=pk)
        message.status = new_status
        logger.debug(message.content)
        
        if new_status == "approved":
            delayed_send_osc_message(
                message.content,
                delay=120,
                message_pk=pk
            )
            
        message.save()
        return True
    except Message.DoesNotExist:
        return False


class MessageListCreateAPIView(APIView):
    """API endpoint for message creation and retrieval"""
    
    def get(self, request) -> Response:
        """Retrieve last 5 messages ordered by creation time"""
        messages = Message.objects.all().order_by('-created_at')[:5]
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request) -> Response:
        """Create new message and forward to Raspberry Pi"""
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            send_message_to_raspberry_pi(serializer.data['content'], message.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageStatusUpdateAPIView(APIView):
    """API endpoint for message status updates"""
    
    def patch(self, request, pk: int) -> Response:
        """Partial update of message status"""
        try:
            new_status = request.data.get('status')
            
            if new_status not in ["received", "approved", "displayed", "rejected"]:
                return Response(
                    {'error': 'Invalid status value'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            update_state(pk, new_status)
            message = Message.objects.get(pk=pk)
            return Response(MessageSerializer(message).data)
            
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class ClearLayerAPIView(APIView):
    """API endpoint for immediate display clearing"""
    
    def post(self, request) -> Response:
        """Clear current display and stop active threads"""
        global active_thread, stop_event, clear_requested, number
        
        if active_thread and active_thread.is_alive():
            update_state(number, "displayed")
            clear_requested = True
            stop_event.set()
            active_thread.join()
            stop_event.clear()
            
        send_osc_message("", "0.0")
        return Response({'status': 'Display cleared successfully'})

class RaspberryLiveAPIView(APIView):
    """API endpoint to check if Raspberry Pi is running"""

    def get(self, request) -> Response:
        """Check the run state of Raspberry Pi"""
        RASPBERRY_PI_URL = "http://192.168.104.212/live"

        try:
            response = requests.get(RASPBERRY_PI_URL, timeout=5)
            if response.status_code == 200:
                return Response({"status": "OK", "code": 200}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"status": "Service Unavailable", "code": 503},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        except requests.RequestException:
            return Response(
                {"status": "Unreachable", "code": 503},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class EmergencyAPIView(APIView):
    """API endpoint for emergency message creation"""
    
    def post(self, request) -> Response:
        """Create new emergency message and forward to Raspberry Pi"""
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            send_message_to_raspberry_pi(serializer.data['content'], message.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)