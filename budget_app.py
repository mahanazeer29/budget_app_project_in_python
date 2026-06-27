class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        """Add a deposit (positive amount) to the ledger."""
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """Add a withdrawal (negative amount) to the ledger if funds allow.

        Returns True if the withdrawal took place, False otherwise.
        """
        if not self.check_funds(amount):
            return False
        self.ledger.append({"amount": -amount, "description": description})
        return True

    def get_balance(self):
        """Return the current balance of the category based on the ledger."""
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, destination_category):
        """Withdraw amount from this category and deposit it into another.

        Returns True if the transfer took place, False otherwise.
        """
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {destination_category.name}")
        destination_category.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount):
        """Return False if amount exceeds the current balance, True otherwise."""
        return amount <= self.get_balance()

    def __str__(self):
        title = self.name.center(30, "*")
        lines = [title]
        for item in self.ledger:
            description = item["description"][:23]
            amount_str = f"{item['amount']:.2f}"[:7]
            spaces = 30 - len(description) - len(amount_str)
            lines.append(f"{description}{' ' * spaces}{amount_str}")
        total = f"Total: {self.get_balance():.2f}"
        lines.append(total)
        return "\n".join(lines)


def create_spend_chart(categories):
    """Build a bar chart (as a string) showing percentage spent by category."""

    # Total withdrawals (as positive numbers) per category
    spent_per_category = []
    for category in categories:
        spent = sum(
            -item["amount"] for item in category.ledger if item["amount"] < 0
        )
        spent_per_category.append(spent)

    total_spent = sum(spent_per_category)

    # Percentage spent per category, rounded down to nearest 10
    percentages = []
    for spent in spent_per_category:
        if total_spent == 0:
            pct = 0
        else:
            pct = (spent / total_spent) * 100
        percentages.append((pct // 10) * 10)

    # Build chart title and y-axis/bars
    chart = "Percentage spent by category\n"

    for value in range(100, -1, -10):
        chart += str(value).rjust(3) + "|"
        for pct in percentages:
            if pct >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    # Horizontal line: 4 spaces (for y-axis label + "|") then dashes
    # 3 chars per category bar + 2 extra chars past the final bar
    chart += "    " + "-" * ((len(categories) * 3) + 1) + "\n"

    # Category names written vertically
    max_name_length = max(len(category.name) for category in categories)
    category_names = [category.name.ljust(max_name_length) for category in categories]

    for i in range(max_name_length):
        chart += "    "
        for name in category_names:
            chart += " " + name[i] + " "
        chart += " \n"
        # Trim trailing space added after final iteration below, handled by final strip

    chart = chart.rstrip("\n")

    return chart
