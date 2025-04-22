class FibonacciSequenceService:
    """Service class for calculating Fibonacci numbers."""

    def get_fib_number(self, index: int) -> int:
        """Returns the Fibonacci number at the given index.

        Args:
            index (int): The index in the Fibonacci sequence (0-based).

        Returns:
            int: The Fibonacci number at the specified index.

        Raises:
            ValueError: If the input index is negative.
        """
        if index < 0:
            raise ValueError("The 'index' argument cannot be negative.")

        if index <= 1:
            return index

        prev2, prev1 = 0, 1
        for _ in range(2, index + 1):
            prev2, prev1 = prev1, prev1 + prev2
        return prev1

    def get_all_fib_numbers(self, index: int) -> list[int]:
        """Returns a list of Fibonacci numbers up to the given index.

        Args:
            number (int): The upper bound index for which to generate Fibonacci numbers.

        Returns:
            list[int]: A list of Fibonacci numbers up to the specified index.

        Raises:
            ValueError: If the input number is negative.
        """
        if index < 0:
            raise ValueError("The 'index' argument cannot be negative.")

        if index == 0:
            return [0]

        fibs = [0, 1]
        for _ in range(2, index + 1):
            fibs.append(fibs[-1] + fibs[-2])
        return fibs
