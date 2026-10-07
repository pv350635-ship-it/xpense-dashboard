from pathlib import Path
import os
from datetime import date
from decimal import Decimal, InvalidOperation

import psycopg
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)


def connect():
    return psycopg.connect(
        host="db",
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


with connect() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            category VARCHAR(100) NOT NULL,
            amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
            expense_date DATE NOT NULL
        )
    """)


PAGE = Path(__file__).with_name("dashboard.html").read_text(encoding="utf-8")


@app.get("/")
def index():
    with connect() as conn:
        expenses = conn.execute("""
            SELECT expense_date, category, amount
            FROM expenses
            ORDER BY expense_date DESC, id DESC
        """).fetchall()

        total = conn.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE expense_date >=
                date_trunc('month', CURRENT_DATE)::date
              AND expense_date <
                (date_trunc('month', CURRENT_DATE)
                 + INTERVAL '1 month')::date
        """).fetchone()[0]

    return render_template_string(
        PAGE, expenses=expenses, total=total, today=date.today()
    )


@app.post("/add")
def add():
    try:
        category = request.form["category"].strip()
        amount = Decimal(request.form["amount"])
        expense_date = date.fromisoformat(request.form["expense_date"])

        if (not category or len(category) > 100
                or not amount.is_finite()
                or amount <= 0
                or amount > Decimal("9999999999.99")):
            raise ValueError()

    except (KeyError, ValueError, InvalidOperation):
        return "Invalid expense details", 400

    with connect() as conn:
        conn.execute(
            """INSERT INTO expenses (category, amount, expense_date)
               VALUES (%s, %s, %s)""",
            (category, amount, expense_date),
        )

    return redirect("/")


@app.get("/health")
def health():
    with connect() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok"}
