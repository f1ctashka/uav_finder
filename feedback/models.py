from django.db import models


class Feedback(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
