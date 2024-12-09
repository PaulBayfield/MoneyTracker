import jwt
import asyncio

from ..components.auth import checkPassword
from sanic import Blueprint, Request, redirect, json
from sanic_ext import render
from datetime import datetime, timedelta
from dotenv import load_dotenv
from json import loads
from os import environ
from random import randint


bp = Blueprint(
    name="User"
)

load_dotenv(dotenv_path=".env")


@bp.post("/user/settings")
async def user_settings(request: Request):
    data = loads(request.body)

    if "theme" in data and data["theme"] in ["light", "dark"]:
        request.ctx.session["theme"] = data.get("theme", request.ctx.session.get("theme", "light"))
    
    if "language" in data and data["language"] in ["fr", "en"]:
        request.ctx.session["language"] = data.get("language", request.ctx.session.get("language", "fr"))

    return json({"success": True})


@bp.get("/user/login")
async def login(request: Request):
    if request.ctx.session.get("user", {}).get("account") is not None:
        return redirect("/")

    return await render(
        "auth/login.html",
        context={
            "session": {
                "theme": request.ctx.session.get("theme", "light"),
                "language": request.ctx.session.get("language", "fr")
            },
            "user": request.ctx.session.get("user", {})
        }
   )


@bp.post("/user/login")
async def loginPost(request: Request):
    username = request.form.get("username")
    password = request.form.get("password")

    data = await checkPassword(request.app, username, password)

    if data:
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.now() + timedelta(days=7)
            }, 
            request.app.config.SECRET
        )

        request.ctx.session["user"] = {
            "username": username,
            "account": data["account"],
            "authenticated": True
        }

        async with request.app.ctx.pool.acquire() as connection:
            await connection.execute(
                "UPDATE users SET token = $1 WHERE username = $2",
                token, username
            )

        response = redirect("/")
        if environ.get("API_DEBUG") == "True":
            response.cookies.add_cookie(
                key="token", 
                value=token,
                httponly=True,
                secure=False,
                max_age=60*60*24*7, # 7 days
                expires=datetime.now() + timedelta(days=7)
            )
        else:
            response.cookies.add_cookie(
                key="token", 
                value=token,
                max_age=60*60*24*7, # 7 days
                expires=datetime.now() + timedelta(days=7)
            )

        return response
    else:
        await asyncio.sleep(randint(1, 3))

        request.ctx.session["user"] = {
            "username": "",
            "authenticated": False
        }

        return redirect("/user/login")


@bp.get("/user/logout")
async def logout(request: Request):
    request.ctx.session["user"] = {
        "username": "",
        "authenticated": False
    }

    response = redirect("/")
    response.cookies.delete_cookie("token")
    return response
