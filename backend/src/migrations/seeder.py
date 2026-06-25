from src.repositories.database import SessionLocal
from src.repositories.schema import MenuItem


MENU_ITEMS = [
    # Coffee
    {"name": "Espresso", "category": "Coffee", "price": 150.0, "description": "Rich, bold single shot of espresso."},
    {"name": "Cappuccino", "category": "Coffee", "price": 280.0, "description": "Espresso with steamed milk foam."},
    {"name": "Latte", "category": "Coffee", "price": 260.0, "description": "Smooth espresso with lots of steamed milk."},
    {"name": "Cold Brew", "category": "Coffee", "price": 220.0, "description": "Slow-steeped cold brew coffee."},
    {"name": "Americano", "category": "Coffee", "price": 180.0, "description": "Espresso diluted with hot water."},
    {"name": "Mocha", "category": "Coffee", "price": 300.0, "description": "Espresso with chocolate and steamed milk."},
    # Food
    {"name": "Pasta", "category": "Food", "price": 320.0, "description": "Creamy pasta with herbs."},
    {"name": "Burger", "category": "Food", "price": 350.0, "description": "Juicy chicken burger with fries."},
    {"name": "Sandwich", "category": "Food", "price": 180.0, "description": "Grilled veggie or chicken sandwich."},
    {"name": "Salad", "category": "Food", "price": 200.0, "description": "Fresh garden salad with dressing."},
    # Dessert
    {"name": "Brownie", "category": "Dessert", "price": 190.0, "description": "Warm chocolate brownie."},
    {"name": "Cheesecake", "category": "Dessert", "price": 240.0, "description": "Classic New York cheesecake slice."},
]


class Seeder:
    def seed_data(self):
        db = SessionLocal()
        try:
            if db.query(MenuItem).count() == 0:
                for item_data in MENU_ITEMS:
                    db.add(MenuItem(**item_data))
                db.commit()
                print("[Seeder] Menu items inserted.")
            else:
                print("[Seeder] Menu items already exist, skipping.")
        finally:
            db.close()
