from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    skills = models.TextField()

    def __str__(self):
        return self.name

class Task(models.Model):
    description = models.TextField()
    assigned_to = models.ForeignKey(TeamMember, on_delete=models.CASCADE, null=True, blank=True)
    deadline = models.CharField(max_length=100)
    priority = models.CharField(max_length=50, default="Medium")
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)