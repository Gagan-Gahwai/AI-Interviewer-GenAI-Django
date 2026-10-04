from django.db import models
from users.models import User
from django.utils import timezone


class InterviewReport(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interview_reports"
    )

    job_description = models.TextField()

    resume = models.TextField(
        blank=True,
        null=True
    )

    self_description = models.TextField(
        blank=True,
        null=True
    )

    match_score = models.IntegerField(
        null=True,
        blank=True
    )

    technical_questions = models.JSONField(
        default=list,
        blank=True
    )

    behavioral_questions = models.JSONField(
        default=list,
        blank=True
    )

    skill_gaps = models.JSONField(
        default=list,
        blank=True
    )

    preparation_plan = models.JSONField(
        default=list,
        blank=True
    )

    title = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title