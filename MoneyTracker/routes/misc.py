from sanic.response import HTTPResponse, redirect, file
from sanic import Blueprint, Request
from sanic_ext import openapi


bp = Blueprint(
    name="Misc",
    url_prefix="/"
)


# /favicon.ico
@bp.route("/favicon.ico", methods=["GET"])
@openapi.no_autodoc
@openapi.exclude()
async def favicon(request: Request) -> HTTPResponse:
    """
    Redirige vers l'icône du site.

    :return: Redirige vers l'icône du site
    """
    return await file(
        location="./static/favicon.ico"
    )
