from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Profile, Skill, Message, MessageRequest, Notification, Project
)


class Command(BaseCommand):
    help = "Add dummy data for SkillSync demo"

    def handle(self, *args, **kwargs):
        people = [
            ("ram", "Ram", "Sharma", "Web developer from Kathmandu.",
             ["Python", "HTML", "CSS"], ["UI/UX", "AI"]),
            ("sita", "Sita", "Thapa", "Graphic designer who loves colors.",
             ["Graphic Design", "Photoshop"], ["Python", "JavaScript"]),
            ("hari", "Hari", "Karki", "Musician and guitar teacher.",
             ["Guitar", "Singing"], ["Video Editing"]),
            ("gita", "Gita", "Rai", "English teacher, loves languages.",
             ["English", "Public Speaking"], ["Django", "Cooking"]),
            ("bikash", "Bikash", "Gurung", "Photographer and traveler.",
             ["Photography", "Video Editing"], ["Guitar", "Excel"]),
            ("anita", "Anita", "Shrestha", "Data analyst, Excel expert.",
             ["Excel", "Data Analysis"], ["Photography", "Python"]),
            ("suman", "Suman", "Adhikari", "Chef and food lover.",
             ["Cooking", "Baking"], ["English", "Marketing"]),
            ("puja", "Puja", "Magar", "Digital marketer.",
             ["Marketing", "Content Writing"], ["Graphic Design"]),
        ]

        users = {}
        for username, first, last, bio, teach, learn in people:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "email": f"{username}@example.com",
                },
            )
            if created:
                user.set_password("test12345")
                user.save()
            users[username] = user

            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "bio": bio,
                    "skills_to_teach": ", ".join(teach),
                    "skills_to_learn": ", ".join(learn),
                },
            )

            for s in teach:
                Skill.objects.get_or_create(user=user, name=s, skill_type="teach")
            for s in learn:
                Skill.objects.get_or_create(user=user, name=s, skill_type="learn")

        projects = [
            ("ram", "Portfolio Website", "Build a personal portfolio together.",
             "HTML, CSS, JavaScript", ["sita", "puja"]),
            ("anita", "Expense Tracker App", "Simple app to track daily expenses.",
             "Python, Excel", ["ram"]),
            ("bikash", "Travel Vlog Series", "Make short travel videos of Nepal.",
             "Photography, Video Editing", ["hari", "puja"]),
        ]
        for owner, title, desc, req, members in projects:
            project, _ = Project.objects.get_or_create(
                owner=users[owner],
                title=title,
                defaults={"description": desc, "required_skills": req},
            )
            for m in members:
                project.members.add(users[m])

        pairs = [
            ("ram", "sita", "Hi Sita! Can you teach me UI design? I can teach Python."),
            ("sita", "ram", "Sure Ram, let's swap skills!"),
            ("hari", "bikash", "Hello! I can teach guitar, want to learn video editing."),
        ]
        for sender, receiver, text in pairs:
            msg, created = Message.objects.get_or_create(
                sender=users[sender],
                receiver=users[receiver],
                content=text,
            )
            if created:
                Notification.objects.create(
                    recipient=users[receiver],
                    sender=users[sender],
                    message=msg,
                )

        MessageRequest.objects.get_or_create(
            sender=users["ram"], receiver=users["sita"], defaults={"status": "accepted"}
        )
        MessageRequest.objects.get_or_create(
            sender=users["hari"], receiver=users["bikash"], defaults={"status": "pending"}
        )
        MessageRequest.objects.get_or_create(
            sender=users["gita"], receiver=users["ram"], defaults={"status": "pending"}
        )

        self.stdout.write(self.style.SUCCESS("Dummy data added successfully!"))