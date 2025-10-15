class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def calculate_price(self, quantity=1):
        return self.price * quantity

    def __str__(self):
        return self.name + " - $" + str(round(self.price, 2))


class Beverage(MenuItem):
    def __init__(self, name, price, size, is_alcoholic):
        super().__init__(name, price)
        self.size = size
        self.is_alcoholic = is_alcoholic

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def get_is_alcoholic(self):
        return self.is_alcoholic

    def set_is_alcoholic(self, is_alcoholic):
        self.is_alcoholic = is_alcoholic

    def __str__(self):
        alcohol = "Alcoholic" if self.is_alcoholic else "Non-Alcoholic"
        return (
            self.name + " (" + self.size + ", " + alcohol + ") - $" + str(round(self.price, 2))
        )


class Appetizer(MenuItem):
    def __init__(self, name, price, is_vegan, portion_size):
        super().__init__(name, price)
        self.is_vegan = is_vegan
        self.portion_size = portion_size

    def get_is_vegan(self):
        return self.is_vegan

    def set_is_vegan(self, is_vegan):
        self.is_vegan = is_vegan

    def get_portion_size(self):
        return self.portion_size

    def set_portion_size(self, portion_size):
        self.portion_size = portion_size

    def __str__(self):
        vegan = "Vegan" if self.is_vegan else "Non-Vegan"
        return (
            self.name + " (" + self.portion_size + ", " + vegan + ") - $" + str(round(self.price, 2))
        )


class MainCourse(MenuItem):
    def __init__(self, name, price, cuisine, calories):
        super().__init__(name, price)
        self.cuisine = cuisine
        self.calories = calories

    def get_cuisine(self):
        return self.cuisine

    def set_cuisine(self, cuisine):
        self.cuisine = cuisine

    def get_calories(self):
        return self.calories

    def set_calories(self, calories):
        self.calories = calories

    def __str__(self):
        return (
            self.name + " (" + self.cuisine + ", " + str(self.calories) + " cal) - $" + str(round(self.price, 2))
        )


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity=1):
        self.items.append((item, quantity))

    def calculate_total_price(self):
        subtotal = sum(item.calculate_price(quantity) for item, quantity in self.items)
        has_main = any(isinstance(item, MainCourse) for item, _ in self.items)
        beverage_discount = 0.0
        if has_main:
            for item, quantity in self.items:
                if isinstance(item, Beverage):
                    beverage_discount += 0.1 * item.calculate_price(quantity)
        total = subtotal - beverage_discount
        return round(total, 2), round(beverage_discount, 2)

    def __str__(self):
        lines = ["Order Summary:"]
        for item, quantity in self.items:
            lines.append("- " + item.name + " x" + str(quantity) + ": $" + str(round(item.calculate_price(quantity), 2)))
        subtotal = sum(item.calculate_price(quantity) for item, quantity in self.items)
        total, beverage_discount = self.calculate_total_price()
        lines.append("Subtotal: $" + str(round(subtotal, 2)))
        if beverage_discount > 0:
            lines.append("Discount (Beverages 10% with MainCourse): $" + str(beverage_discount))
        lines.append("Total: $" + str(total))
        return "\n".join(lines)


class Payment:
    def __init__(self, order, method):
        self.order = order
        self.method = method
        self.amount_paid = 0.0

    def get_method(self):
        return self.method

    def set_method(self, method):
        self.method = method

    def get_amount_paid(self):
        return self.amount_paid

    def set_amount_paid(self, amount):
        self.amount_paid = amount

    def process_payment(self):
        total, _ = self.order.calculate_total_price()
        self.amount_paid = total
        return "Payment of $" + str(round(total, 2)) + " processed via " + self.method

    def __str__(self):
        return "Payment Method: " + self.method + " | Amount Paid: $" + str(round(self.amount_paid, 2))


def create_menu():
    return [
        Beverage("Coca-Cola", 2.5, "Medium", False),
        Beverage("Lemonade", 2.0, "Small", False),
        Beverage("Beer", 3.5, "Large", True),
        Appetizer("French Fries", 3.5, True, "Medium"),
        Appetizer("Chicken Tenders", 5.0, False, "Large"),
        MainCourse("Cheeseburger", 8.5, "American", 850),
        MainCourse("Spaghetti", 9.0, "Italian", 700),
    ]


if __name__ == "__main__":
    order = Order()
    menu = create_menu()
    order.add_item(menu[0], 2)
    order.add_item(menu[2], 1)
    order.add_item(menu[3], 1)
    order.add_item(menu[5], 1)
    print(order)
    payment = Payment(order, "Credit Card")
    print(payment.process_payment())
    print(payment)
