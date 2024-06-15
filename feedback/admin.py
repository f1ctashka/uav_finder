from django.contrib import admin
from feedback.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "username")

    @staticmethod
    def username(obj: Feedback) -> str:
        return obj.user.username
