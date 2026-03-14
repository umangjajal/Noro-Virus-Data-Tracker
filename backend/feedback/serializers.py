from rest_framework import serializers

class FeedbackSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    type = serializers.CharField(max_length=50) # e.g., Bug, Suggestion, Other
    message = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
