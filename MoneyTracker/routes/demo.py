from ..components.auth import authenticated
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, redirect
from sanic_ext import render
from datetime import datetime, timedelta


bp = Blueprint(
    name="Demo",
)


# /demo
@bp.route("/demo", methods=["GET"])
async def demo(request: Request) -> HTTPResponse:
    transactions = [
        {'id': '1', 'label': 'EXPO', 'booking_date_time': '2024-04-26T00:00:00.000000', 'amount': -413.25, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '2', 'label': 'KINEPOLIS', 'booking_date_time': '2023-06-18T00:00:00.000000', 'amount': 4.06, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '3', 'label': 'COIFFURE', 'booking_date_time': '2024-09-03T00:00:00.000000', 'amount': 341.78, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '4', 'label': 'DIRECT ENERGIE', 'booking_date_time': '2024-11-23T00:00:00.000000', 'amount': 317.53, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '5', 'label': 'SALON', 'booking_date_time': '2023-07-11T00:00:00.000000', 'amount': -307.26, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '6', 'label': 'COIFFURE', 'booking_date_time': '2024-09-27T00:00:00.000000', 'amount': -446.14, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '7', 'label': 'COIFFURE', 'booking_date_time': '2024-02-08T00:00:00.000000', 'amount': 196.18, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '8', 'label': 'PHARMACIES', 'booking_date_time': '2024-12-05T00:00:00.000000', 'amount': 205.34, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '9', 'label': 'SODEXO', 'booking_date_time': '2024-09-06T00:00:00.000000', 'amount': -90.25, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '10', 'label': 'ENI', 'booking_date_time': '2024-01-15T00:00:00.000000', 'amount': 131.6, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '11', 'label': 'DISNEYLAND', 'booking_date_time': '2023-09-12T00:00:00.000000', 'amount': -427.61, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '12', 'label': 'COIFFURE', 'booking_date_time': '2023-08-26T00:00:00.000000', 'amount': 223.61, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '13', 'label': 'COIFFURE', 'booking_date_time': '2024-07-18T00:00:00.000000', 'amount': 292.49, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '14', 'label': 'LECLERC', 'booking_date_time': '2024-02-04T00:00:00.000000', 'amount': 467.39, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '15', 'label': 'INTERMARCHE', 'booking_date_time': '2023-10-29T00:00:00.000000', 'amount': 329.59, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '16', 'label': 'YOUTUBE', 'booking_date_time': '2024-11-11T00:00:00.000000', 'amount': 448.27, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '17', 'label': 'EXPO', 'booking_date_time': '2024-05-11T00:00:00.000000', 'amount': -203.36, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '18', 'label': 'AUTOROUTE', 'booking_date_time': '2023-07-13T00:00:00.000000', 'amount': 184.19, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '19', 'label': 'RUSSE', 'booking_date_time': '2024-04-04T00:00:00.000000', 'amount': -5.66, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '20', 'label': 'TGV', 'booking_date_time': '2023-06-19T00:00:00.000000', 'amount': 410.33, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '21', 'label': 'COIFFURE', 'booking_date_time': '2023-08-08T00:00:00.000000', 'amount': -437.68, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '22', 'label': 'NEKOROCK', 'booking_date_time': '2024-03-18T00:00:00.000000', 'amount': 426.27, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '23', 'label': 'UGC', 'booking_date_time': '2023-07-09T00:00:00.000000', 'amount': 350.66, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '24', 'label': 'YOUTUBE', 'booking_date_time': '2024-12-03T00:00:00.000000', 'amount': -163.53, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '25', 'label': 'VTC', 'booking_date_time': '2023-07-09T00:00:00.000000', 'amount': -287.83, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '26', 'label': 'KEBAB', 'booking_date_time': '2024-08-06T00:00:00.000000', 'amount': -176.69, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '27', 'label': 'RESTAURANT', 'booking_date_time': '2024-01-23T00:00:00.000000', 'amount': 487.65, 'amount_currency': 'EUR', 'nature': 'credit'},
        {'id': '28', 'label': 'AMERICAIN', 'booking_date_time': '2024-11-28T00:00:00.000000', 'amount': -216.71, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '29', 'label': 'COIFFURE', 'booking_date_time': '2023-11-13T00:00:00.000000', 'amount': -189.59, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '30', 'label': 'PHARMACIES', 'booking_date_time': '2023-08-01T00:00:00.000000', 'amount': -375.6, 'amount_currency': 'EUR', 'nature': 'debit'},
        {'id': '31', 'label': 'Random', 'booking_date_time': datetime.now().isoformat(), 'amount': -30.0, 'amount_currency': 'EUR', 'nature': 'credit'},
    ]

    transactions.sort(key=lambda x: x['booking_date_time'])
    
    balance = 50

    return await render(
        "dashboard/demo.html",
        context={
            "session": {
                "theme": "light",
                "language": "fr"
            },
            "data": {
                "account": "00000000001",
                "user": "Demo User",
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
                "transaction_from": datetime.strptime(transactions[-1]["booking_date_time"].split("T")[0], "%Y-%m-%d").strftime("%d/%m/%Y") if transactions else datetime.now().strftime("%d/%m/%Y"),
                "labels": request.app.ctx.labels,
            }
        }
   )
