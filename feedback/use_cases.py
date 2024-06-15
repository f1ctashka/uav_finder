from feedback.models import Feedback
from users.models import User


class CreateFeedbackUseCaseImpl:
    def __call__(self, subject: str, message: str, user: User) -> None:
        Feedback.objects.create(subject=subject, message=message, user=user)
