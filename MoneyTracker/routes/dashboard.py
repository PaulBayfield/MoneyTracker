from ..components.auth import authenticated
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, redirect
from sanic_ext import render
from datetime import datetime, timedelta


bp = Blueprint(
    name="Dashboard",
)


# /
@bp.route("/", methods=["GET"])
@authenticated
async def index(request: Request) -> HTTPResponse:
    if request.ctx.session.get("user", {}).get("account") is None:
        return redirect("/user/login")

    async with request.app.ctx.pool.acquire() as connection:
        async with connection.transaction():
            balance = await connection.fetchval("SELECT balance FROM accounts WHERE id = $1", request.ctx.session["user"]["account"])
            user = await connection.fetchval("SELECT username FROM accounts WHERE id = $1", request.ctx.session["user"]["account"])
            records_transactions = await connection.fetch("SELECT * FROM transactions WHERE user_id = $1 ORDER BY booking_date_time DESC", request.ctx.session["user"]["account"])


    transactions = [
        {
            'id': str(t['id']),
            'label': t['label'],
            'booking_date_time': t['booking_date_time'].isoformat(),
            'amount': float(t['amount']),
            'amount_currency': t['amount_currency'],
            'nature': t['nature']
        } for t in records_transactions
    ]
    transactions.reverse()

    return await render(
        "dashboard/dashboard.html",
        context={
            "session": {
                "theme": request.ctx.session.get("theme", "light"),
                "language": request.ctx.session.get("language", "fr")
            },
            "data": {
                "account": request.ctx.session["user"]["account"],
                "user": user,
                "received": {
                    "today": sum([float(t["amount"]) for t in transactions if t["booking_date_time"].split("T")[0] == datetime.now().isoformat().split("T")[0] and float(t["amount"]) > 0]),
                    "last_day": sum([float(t["amount"]) for t in transactions if t["booking_date_time"].split("T")[0] == (datetime.now() - timedelta(days=1)).isoformat().split("T")[0] and float(t["amount"]) > 0]),
                    "week": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").isocalendar()[1] == datetime.now().isocalendar()[1] and float(t["amount"]) > 0]),
                    "last_week": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").isocalendar()[1] == datetime.now().isocalendar()[1] - 1 and float(t["amount"]) > 0]),
                    "month": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").month == datetime.now().month and float(t["amount"]) > 0]),
                    "last_month": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").month == datetime.now().month - 1 and float(t["amount"]) > 0]),
                    "year": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").year == datetime.now().year and float(t["amount"]) > 0]),
                    "last_year": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").year == datetime.now().year - 1 and float(t["amount"]) > 0])
                },
                "spent": {
                    "today": sum([float(t["amount"]) for t in transactions if t["booking_date_time"].split("T")[0] == datetime.now().isoformat().split("T")[0] and float(t["amount"]) < 0]),
                    "last_day": sum([float(t["amount"]) for t in transactions if t["booking_date_time"].split("T")[0] == (datetime.now() - timedelta(days=1)).isoformat().split("T")[0] and float(t["amount"]) < 0]),
                    "week": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").isocalendar()[1] == datetime.now().isocalendar()[1] and float(t["amount"]) < 0]),
                    "last_week": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").isocalendar()[1] == datetime.now().isocalendar()[1] - 1 and float(t["amount"]) < 0]),
                    "month": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").month == datetime.now().month and float(t["amount"]) < 0]),
                    "last_month": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").month == datetime.now().month - 1 and float(t["amount"]) < 0]),
                    "year": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").year == datetime.now().year and float(t["amount"]) < 0]),
                    "last_year": sum([float(t["amount"]) for t in transactions if datetime.strptime(t["booking_date_time"].split("T")[0], "%Y-%m-%d").year == datetime.now().year - 1 and float(t["amount"]) < 0])
                },
                "balance": balance,
                "transactions": transactions,
                "transaction_from": records_transactions[-1]["booking_date_time"].strftime("%d/%m/%Y") if records_transactions else datetime.now().strftime("%d/%m/%Y"),
                "labels": request.app.ctx.labels,
            },
            "user": request.ctx.session.get("user", {})
        }
   )
