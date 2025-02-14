from django.db import models

from django.db import models

class Message(models.Model):
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('received', 'Received'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('sent', 'Sent'),  ('displayed', 'Displayed')],
        default='sent'
    )

