from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .customer import Customer


def _truncate_float(value: float | int) -> float | int:
    if value == int(value):
        return int(value)
    return value


@dataclass
class Shop:
    name: str
    location: list[int]
    products: dict[str, int | float]

    @classmethod
    def from_dict(cls, dict_: dict) -> Shop:
        return cls(**dict_)

    def get_products_costs(
        self, products: dict[str, int]
    ) -> dict[str, int | float]:
        try:
            return {
                product: self.products[product] * quantity
                for product, quantity in products.items()
            }
        except KeyError as e:
            raise NoProductException(e.args[0]) from e

    def serve_customer(self, customer: Customer) -> None:
        print("Date:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print(f"Thanks, {customer.name}, for your purchase!")
        print("You have bought:")

        costs = self.get_products_costs(customer.product_cart)
        for product, cost in costs.items():
            print(
                f"{customer.product_cart[product]} {product}s"
                f" for {_truncate_float(cost)} dollars"
            )

        total_cost = sum(costs.values())
        print(f"Total cost is {total_cost} dollars")
        customer.money -= total_cost
        customer.product_cart.clear()
        print("See you again!")


class NoProductException(Exception):
    """This exception occurs when requested product is not in the shop"""
