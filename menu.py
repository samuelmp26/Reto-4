class MenuItem:
    def __init__(self, name, price):
        self.name = name
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

    def __str__(self):
        alcohol = "Alcoholic" if self.is_alcoholic else "Non-Alcoholic"
        return (
            self.name + " (" + self.size + ", "
            + alcohol + ") - $" + str(round(self.price, 2))
        )


class Appetizer(MenuItem):
    def __init__(self, name, price, is_vegan, portion_size):
        super().__init__(name, price)
        self.is_vegan = is_vegan
        self.portion_size = portion_size

    def __str__(self):
        vegan = "Vegan" if self.is_vegan else "Non-Vegan"
        return (
            self.name + " (" + self.portion_size + ", "
            + vegan + ") - $" + str(round(self.price, 2))
        )


class MainCourse(MenuItem):
    def __init__(self, name, price, cuisine, calories):
        super().__init__(name, price)
        self.cuisine = cuisine
        self.calories = calories

    def __str__(self):
        return (
            self.name + " (" + self.cuisine + ", "
            + str(self.calories) + " cal) - $" + str(round(self.price, 2))
        )


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity=1):
        self.items.append((item, quantity))

    def beverage_discount(self):
        discount = 0.0
        for item, quantity in self.items:
            if isinstance(item, Beverage):
                discount += 0.1 * item.calculate_price(quantity)
        return discount

    def appetizer_main_combo_discount(self):
        appetizer_count = sum(
            quantity for item, quantity in self.items if isinstance(item, Appetizer)
        )
        main_prices = []
        for item, quantity in self.items:
            if isinstance(item, MainCourse):
                main_prices.extend([item.price] * quantity)
        pairs = min(appetizer_count, len(main_prices))
        if pairs <= 0:
            return 0.0
        main_prices.sort()
        discount = sum(0.1 * price for price in main_prices[:pairs])
        return discount

    def extra_total_discount(self, subtotal_after_other_discounts):
        if subtotal_after_other_discounts > 50:
            return 0.1 * subtotal_after_other_discounts
        return 0.0

    def calculate_total(self):
        subtotal = sum(
            item.calculate_price(quantity) for item, quantity in self.items
        )
        discount_beverage = self.beverage_discount()
        discount_combo = self.appetizer_main_combo_discount()
        subtotal_after = subtotal - discount_beverage - discount_combo
        discount_extra = self.extra_total_discount(subtotal_after)
        total = subtotal_after - discount_extra
        return round(total, 2)

    def __str__(self):
        lines = ["Order Summary:"]
        for item, quantity in self.items:
            lines.append("- " + item.name
                         + " x" + str(quantity)
                         + ": $" + str(round(item.calculate_price(quantity), 2)))
        subtotal = sum(item.calculate_price(quantity) for item, quantity in self.items)
        discount_beverage = self.beverage_discount()
        discount_combo = self.appetizer_main_combo_discount()
        subtotal_after = subtotal - discount_beverage - discount_combo
        discount_extra = self.extra_total_discount(subtotal_after)
        lines.append("Subtotal: $" + str(round(subtotal, 2)))
        if discount_beverage > 0:
            lines.append("Discount (Beverages 10%): $" + str(round(discount_beverage, 2)))
        if discount_combo > 0:
            lines.append("Discount (Appetizer+Main combo): $" + str(round(discount_combo, 2)))
        if discount_extra > 0:
            lines.append("Discount (Extra > $50): $" + str(round(discount_extra, 2)))
        lines.append("Total: $" + str(round(self.calculate_total(), 2)))
        return "\n".join(lines)


#Esto es una prueba con algunos items del menu y cantidades para verificarlo
def create_menu():
    return [
        Beverage("Coca-Cola", 2.5, "Medium", False),
        Beverage("Lemonade", 2.0, "Small", False),
        Beverage("Coffee", 1.8, "Small", False),
        Beverage("Beer", 3.5, "Large", True),
        Appetizer("French Fries", 3.5, True, "Medium"),
        Appetizer("Chicken Tenders", 5.0, False, "Large"),
        Appetizer("Spring Rolls", 4.5, True, "Small"),
        MainCourse("Cheeseburger", 8.5, "American", 850),
        MainCourse("Spaghetti", 9.0, "Italian", 700),
        MainCourse("Curry Chicken", 10.0, "Indian", 900),
    ]


if __name__ == "__main__":
    print("\nCreating an order...\n")
    order = Order()
    order.add_item(create_menu()[0], 2)   # 2 Coca-Cola
    order.add_item(create_menu()[3], 1)   # 1 Beer
    order.add_item(create_menu()[4], 2)   # 2 French Fries
    order.add_item(create_menu()[7], 1)   # 1 Cheeseburger
    order.add_item(create_menu()[8], 1)   # 1 Spaghetti

    print(order)



#Esto me ayudo con ciertos errores como decimales gigantes en los descuentos y
#detalles en la impresion del resumen de la orden.