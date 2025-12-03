import sqlite3
from fastapi import FastAPI

'''Работа с базой данных Sqlite3'''
def get_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
def get_data():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
    SELECT * FROM sales
    ''')
    rows = c.fetchall()
    saless = []
    for row in rows:
        saless.append(dict(row))
    conn.close()
    return saless

'''Работа с данными в формате словарей'''
def get_sales_stats():
    sales = get_data()
    total_amount = 0
    categories = set(sale["category"] for sale in sales)
    category_stats = {x: 0 for x in categories}
    most_expensive_sale = max(sales, key=lambda sale: sale["amount"])
    for sale in sales:
        total_amount += sale["amount"]
        category_stats[sale["category"]] += sale["amount"]
    total_stats = {
        "total_amount": total_amount,
        "category_stats": category_stats,
        "most_expensive_sale": most_expensive_sale,
    }
    return total_stats

'''Работа с FastApi'''
app = FastAPI()
@app.get("/")
def get_app():
    return {"app": "zhan lox"}

@app.get("/sales")
def get_sales():
    return get_data()

@app.get("/total_stats")
def get_total_stats():
    return get_sales_stats()
