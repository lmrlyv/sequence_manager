from django.db import models


class BlacklistedFibonacciNumber(models.Model):
    """Represents a Fibonacci number that has been blacklisted.

    This model is used to store Fibonacci numbers that should be excluded from certain operations,
    such as listing or calculation. Each number is stored as a unique positive integer.
    """

    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.number)
