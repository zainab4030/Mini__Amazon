
# orders.py
from datetime import datetime
from storage import load_json, save_json

ORDERS_PATH = "data/orders.json"

class OrderManager:
    def __init__(self):
        self.orders = load_json(ORDERS_PATH, default=[])
        self.current_user = "zainab"  # Your username

    def _save(self):
        save_json(ORDERS_PATH, self.orders)

    def _next_order_id(self) -> str:
        n = len(self.orders) + 1
        return f"O{n:04d}"

    def history_for_user(self, username: str):
        return [o for o in self.orders if o["username"] == username]

    def checkout(self, username: str, cart: dict, catalog):
        if not cart:
            return False, "Cart is empty.", None

        # Validate stock
        for pid, qty in cart.items():
            p = catalog.get_by_id(pid)
            if not p or qty > p["stock"]:
                return False, f"Not enough stock for {p['name'] if p else pid}.", None

        # Create order
        order_id = self._next_order_id()
        items = []
        total = 0.0
        
        for pid, qty in cart.items():
            p = catalog.get_by_id(pid)
            catalog.deduct_stock(pid, qty)
            item = {
                "name": p["name"],
                "qty": qty,
                "unit_price": p["price"]
            }
            items.append(item)
            total += p["price"] * qty

        # Save order
        order = {
            "username": username,
            "order_id": order_id,
            "items": items,
            "total": round(total, 2),
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.orders.append(order)
        self._save()

        self.print_receipt(order)
        
        return True, "Checkout successful!", order

    

    def print_receipt(self, order):
        print("\n" + "="*50)
        print("           RECEIPT           ")
        print("="*50)
        print(f"Customer: {order['username']}")
        print(f"Order ID: {order['order_id']}")
        print(f"Items: {len(order['items'])}")
        print("-" * 35)

        for item in order['items']:
            print(f"- {item['name']} x{item['qty']}  €{item['unit_price']:.2f}")

        print("-" * 35)
        print(f"TOTAL: €{order['total']:.2f}")
        print(f"Date: {order['date_time']}")
        print("="*50)
        print("Thank you for shopping!")
        print("="*50 + "\n")