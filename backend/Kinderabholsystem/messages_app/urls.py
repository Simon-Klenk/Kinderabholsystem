from django.urls import path
from .views import MessageListCreateAPIView, MessageStatusUpdateAPIView, ClearLayerAPIView

urlpatterns = [
    path('messages/', MessageListCreateAPIView.as_view(), name='message_list_create'),
    path('messages/<int:pk>/', MessageStatusUpdateAPIView.as_view(), name='message_status_update'),
    path('clear/', ClearLayerAPIView.as_view(), name='clear_layer'),
]

