from django.db import models

class Feedback(models.Model):
    # Note: These fields are mirrors for Mongo document structures.
    # In MongoDB, we use pymongo for the main flow, but these are 
    # useful for documenting our schema and if we use hybrid SQL/NoSQL storage.
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback_type = models.CharField(max_length=50) # Bug, Suggestion, Other
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.feedback_type} from {self.name}"

    class Meta:
        ordering = ['-created_at']
