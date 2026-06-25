"""
BeanBrew MCP Server
Exposes coffee shop tools, prompts, and resources via Model Context Protocol.
"""
# from __future__ import annotations

import os
import json
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/beanbrew")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

mcp = FastMCP("BeanBrew Coffee Shop")


def get_db() -> Session:
    return SessionLocal()


# ── PROMPTS ────────────────────────────────────────────────────────────────────

@mcp.prompt("order_assistant")
def order_assistant_prompt(customer_name: str = "valued customer") -> str:
    return f"""You are BeanBrew's warm and friendly coffee shop assistant helping {customer_name}. ☕

Your personality:
- Enthusiastic about coffee and good food
- Helpful, patient, and precise with orders  
- Use ☕🌿🍰 emojis occasionally for warmth
- Always confirm order details clearly

Your capabilities:
- Show the menu (use get_menu tool or the menu resource)
- Place orders (use create_order tool)
- Check order status (use check_order_status tool)
- Retrieve last order (use get_last_order tool)

When placing orders, extract item names and quantities from the customer's message.
Always confirm the order was placed successfully with order ID, items, total, and status."""


@mcp.prompt("order_summary")
def order_summary_prompt(order_id: str = "") -> str:
    if order_id:
        return f"Provide a friendly summary of order #{order_id} including all items, quantities, prices, and current status."
    return "Provide a friendly summary of the most recent order."


# ── RESOURCES ──────────────────────────────────────────────────────────────────

@mcp.resource("coffeeshop://menu")
def get_menu_resource() -> str:
    db = get_db()
    try:
        rows = db.execute(
            text("SELECT name, category, price, description FROM menu_items WHERE is_available = TRUE ORDER BY category, price")
        ).fetchall()

        menu: dict[str, list] = {}
        for row in rows:
            cat = row[1]
            if cat not in menu:
                menu[cat] = []
            menu[cat].append({"name": row[0], "price": row[2], "description": row[3]})

        lines = ["=== BeanBrew Menu ==="]
        for category, items in menu.items():
            lines.append(f"\n{category}:")
            for item in items:
                lines.append(f"  • {item['name']} — ₹{item['price']:.0f}  ({item['description']})")
        return "\n".join(lines)
    finally:
        db.close()


@mcp.resource("coffeeshop://shop_info")
def get_shop_info_resource() -> str:
    return """=== BeanBrew Coffee Shop ===
Location: 42 Brew Street, Coimbatore, Tamil Nadu
Hours: Mon–Sat 7:00 AM – 10:00 PM | Sun 8:00 AM – 9:00 PM
Phone: +91-422-000-1234
WiFi: BeanBrew_Guest (password: coffee123)
Speciality: Single-origin espresso, artisan pastries, and cozy vibes.
Loyalty: Earn 1 point per ₹10 spent. 100 points = ₹50 off!"""


# ── TOOLS ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_menu() -> str:
    """Get the full BeanBrew menu with all available items and prices."""
    return get_menu_resource()


@mcp.tool()
def create_order(customer_id: int, item_names: str, quantities: str) -> str:
    """
    Place a new order for the customer.
    
    Args:
        customer_id: The customer's ID
        item_names: Comma-separated item names e.g. "Cappuccino,Brownie"
        quantities: Comma-separated quantities e.g. "2,1"
    
    Returns:
        Order confirmation with order ID, items, total, and status.
    """
    db = get_db()
    try:
        names = [n.strip() for n in item_names.split(",")]
        qtys = [int(q.strip()) for q in quantities.split(",")]

        if len(names) != len(qtys):
            return "Error: item_names and quantities must have the same count."

        # Look up items
        order_items_data = []
        total = 0.0
        for name, qty in zip(names, qtys):
            row = db.execute(
                text("SELECT item_id, name, price FROM menu_items WHERE LOWER(name) = LOWER(:name) AND is_available = TRUE"),
                {"name": name}
            ).fetchone()
            if not row:
                return f"Sorry, '{name}' is not available on our menu. Please check the menu and try again."
            subtotal = row[2] * qty
            total += subtotal
            order_items_data.append({"item_id": row[0], "name": row[1], "price": row[2], "qty": qty, "subtotal": subtotal})

        # Create order
        result = db.execute(
            text("INSERT INTO orders (customer_id, status, total_amount, created_at, updated_at) VALUES (:cid, 'PENDING', :total, NOW(), NOW()) RETURNING order_id"),
            {"cid": customer_id, "total": total}
        )
        order_id = result.fetchone()[0]

        # Create order items
        for item in order_items_data:
            db.execute(
                text("INSERT INTO order_items (order_id, item_id, quantity, unit_price) VALUES (:oid, :iid, :qty, :price)"),
                {"oid": order_id, "iid": item["item_id"], "qty": item["qty"], "price": item["price"]}
            )

        db.commit()

        lines = [f"✅ Order #{order_id} placed successfully!\n"]
        for item in order_items_data:
            lines.append(f"  • {item['qty']}x {item['name']} — ₹{item['subtotal']:.0f}")
        lines.append(f"\n💰 Total: ₹{total:.0f}")
        lines.append("📋 Status: PENDING")
        lines.append("\nYour order is being prepared. Thank you for choosing BeanBrew! ☕")

        return "\n".join(lines)

    except Exception as e:
        db.rollback()
        return f"Failed to place order: {str(e)}"
    finally:
        db.close()


@mcp.tool()
def check_order_status(order_id: int) -> str:
    """
    Check the current status of a specific order.
    
    Args:
        order_id: The order ID to check
    
    Returns:
        Order details including status, items, and total.
    """
    db = get_db()
    try:
        order = db.execute(
            text("SELECT order_id, customer_id, status, total_amount, created_at FROM orders WHERE order_id = :oid"),
            {"oid": order_id}
        ).fetchone()

        if not order:
            return f"Order #{order_id} not found."

        items = db.execute(
            text("""
                SELECT mi.name, oi.quantity, oi.unit_price
                FROM order_items oi
                JOIN menu_items mi ON oi.item_id = mi.item_id
                WHERE oi.order_id = :oid
            """),
            {"oid": order_id}
        ).fetchall()

        status_emoji = {"PENDING": "⏳", "PREPARING": "👨‍🍳", "READY": "✅", "DELIVERED": "🎉"}.get(order[2], "📋")

        lines = [f"Order #{order[0]} {status_emoji}"]
        lines.append(f"Status: {order[2]}")
        lines.append(f"Placed: {order[4].strftime('%d %b %Y, %I:%M %p')}")
        lines.append("\nItems:")
        for item in items:
            lines.append(f"  • {item[1]}x {item[0]} — ₹{item[1]*item[2]:.0f}")
        lines.append(f"\nTotal: ₹{order[3]:.0f}")

        return "\n".join(lines)

    finally:
        db.close()


@mcp.tool()
def get_last_order(customer_id: int) -> str:
    """
    Get the most recent order for a customer.
    
    Args:
        customer_id: The customer's ID
    
    Returns:
        Details of the most recent order.
    """
    db = get_db()
    try:
        order = db.execute(
            text("SELECT order_id, status, total_amount, created_at FROM orders WHERE customer_id = :cid ORDER BY created_at DESC LIMIT 1"),
            {"cid": customer_id}
        ).fetchone()

        if not order:
            return "You haven't placed any orders yet. Check out our menu and place your first order! ☕"

        items = db.execute(
            text("""
                SELECT mi.name, oi.quantity, oi.unit_price
                FROM order_items oi
                JOIN menu_items mi ON oi.item_id = mi.item_id
                WHERE oi.order_id = :oid
            """),
            {"oid": order[0]}
        ).fetchall()

        lines = [f"Your last order was Order #{order[0]}"]
        lines.append(f"Status: {order[1]}")
        lines.append(f"Placed: {order[3].strftime('%d %b %Y, %I:%M %p')}")
        lines.append("\nItems:")
        for item in items:
            lines.append(f"  • {item[1]}x {item[0]} — ₹{item[1]*item[2]:.0f}")
        lines.append(f"\nTotal: ₹{order[2]:.0f}")
        lines.append("\nWould you like to reorder the same items?")

        return "\n".join(lines)

    finally:
        db.close()


import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    print(f"[BeanBrew MCP] Starting on 0.0.0.0:{port}...")
    
    app = mcp.streamable_http_app()
    uvicorn.run(app, host="0.0.0.0", port=port)