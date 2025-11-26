from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    estimated_hours = models.IntegerField()
    # Importance is 1-10 scale as per requirements
    importance = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    # We store dependencies as a simple text list of IDs for this assignment to keep it simple
    # Example input: "1,4,5"
    dependencies = models.CharField(max_length=200, blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title