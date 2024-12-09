from sanic import Sanic, Request
from sanic_session import Session, InMemorySessionInterface
from .config import AppConfig
from .routes import RouteDashboard, RouteMisc, RouteUser, RouteDemo
from .utils.logger import Logger
from .utils.worker import Worker
from dotenv import load_dotenv
from os import environ
from asyncpg import create_pool
from datetime import datetime
from pytz import timezone
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler as Scheduler
from apscheduler.triggers.interval import IntervalTrigger


load_dotenv(dotenv_path=f".env")


# Initialisation de l'application
app = Sanic(
    name="MoneyTracker",
    config=AppConfig(),
)

app.config.SECRET = environ["APP_SECRET"]


Session(app, interface=InMemorySessionInterface())


# Enregistrement des routes
app.blueprint(RouteDashboard)
app.blueprint(RouteMisc)
app.blueprint(RouteUser)
app.blueprint(RouteDemo)

app.static("/static", "./static")


# Labels
app.ctx.labels = {
    "🍎 • Alimentation": environ["LABEL_ALIMENTATION"].split(","),
    "🚗 • Transport": environ["LABEL_TRANSPORT"].split(","),
    "🏠 • Logement": environ["LABEL_LOGEMENT"].split(","),
    "📺 • Abonnements": environ["LABEL_ABONNEMENTS"].split(","),
    "🎉 • Loisirs": environ["LABEL_LOISIRS"].split(","),
    "🍽️ • Restaurants": environ["LABEL_RESTAURANTS"].split(","),
    "💊 • Santé": environ["LABEL_SANTE"].split(","),
    "✨ • Divers": environ["LABEL_DIVERS"].split(","),
    "🛍️ • Achats": environ["LABEL_ACHATS"].split(","),
    "💰 • Épargne": environ["LABEL_EPARGNE"].split(","),
}


@app.listener("before_server_start")
async def setup_app(app: Sanic, loop):
    app.ctx.logs = Logger("logs")
    app.ctx.requests = Logger("requests")
    app.ctx.session = ClientSession()

    # Chargement de la base de données
    try:
        app.ctx.pool = await create_pool(
            database=environ["POSTGRES_DATABASE"], 
            user=environ["POSTGRES_USER"], 
            password=environ["POSTGRES_PASSWORD"], 
            host=environ["POSTGRES_HOST"],
            port=environ["POSTGRES_PORT"],
            min_size=10,        # 10 connections
            max_size=10,        # 10 connections
            max_queries=50000,  # 50,000 queries
            loop=loop
        )
    except OSError:
        app.ctx.logs.error("Impossible de se connecter à la base de données !")
        app.ctx.logs.debug("Arrêt de l'API !")
        exit(1)


    app.ctx.worker = Worker(app.ctx.pool, app.ctx.logs)
    await app.ctx.worker.run()
    app.ctx.scheduler = Scheduler()

    app.ctx.scheduler.add_job(app.ctx.worker.run, IntervalTrigger(seconds=int(environ.get("CACHE", 86400))), id="cache")
    app.ctx.scheduler.start()

    app.ctx.logs.info("API démarrée")


@app.listener("after_server_stop")
async def close_app(app: Sanic, loop):
    await app.ctx.pool.close()
    await app.ctx.session.close()

    app.ctx.logs.info("API arrêtée")


@app.on_request
async def before_request(request: Request):
    request.ctx.start = datetime.now(timezone("Europe/Paris")).timestamp()


@app.on_response
async def after_request(request: Request, response):
    end = datetime.now(timezone("Europe/Paris")).timestamp()
    process = end - request.ctx.start

    app.ctx.requests.info(f"{request.headers.get('CF-Connecting-IP', request.client_ip)} - [{request.method}] {request.url} - {response.status} ({process * 1000:.2f}ms)")
