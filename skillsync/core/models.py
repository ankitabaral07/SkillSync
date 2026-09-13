from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    bio = models.TextField(
        blank=True
    )

    skills_to_teach = models.TextField(
        blank=True,
        help_text="Example: Python, HTML, CSS, JavaScript"
    )

    skills_to_learn = models.TextField(
        blank=True,
        help_text="Example: Django, AI, UI/UX"
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class Skill(models.Model):

    SKILL_TYPE_CHOICES = [
        ('teach', 'Can Teach'),
        ('learn', 'Want to Learn'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='skills'
    )

    name = models.CharField(
        max_length=100
    )

    skill_type = models.CharField(
        max_length=10,
        choices=SKILL_TYPE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.skill_type})"


class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"


class MessageRequest(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_requests'
    )

    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('deleted', 'Deleted'),
            ('blocked', 'Blocked'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} ({self.status})"


class Notification(models.Model):

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    notification_type = models.CharField(
        max_length=20,
        default='message'
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}"

class Project(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    required_skills = models.CharField(
        max_length=300,
        blank=True
    )

    members = models.ManyToManyField(
        User,
        related_name='joined_projects',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title   