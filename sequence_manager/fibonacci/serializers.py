from rest_framework import serializers


class FibonacciNumberSerializer(serializers.Serializer):
    number = serializers.IntegerField(
        min_value=1, help_text="Must be a positive integer (1 or greater)."
    )
