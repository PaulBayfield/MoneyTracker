import jwt

from functools import wraps
from sanic import Request, redirect


def checkToken(request: Request) -> bool:
    """
    Check if the user has a valid token

    :param request: Request object
    :return: True if the user has a valid token, False otherwise
    """
    if not request.cookies.get("token"):
        return False

    try:
        jwt.decode(
            request.cookies.get("token"), request.app.config.SECRET, algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


async def checkPassword(app, user: str, password: str) -> dict:
    """
    Check if the user has a valid password

    :param app: Sanic app object
    :param user: Username
    :param password: Password
    :return: Dictionary containing the username and admin status of the user
    """
    async with app.ctx.pool.acquire() as connection:
        data = await connection.fetchrow(
            "SELECT username, account FROM users WHERE username = $1 AND password = crypt($2, password)",
            user, password
        )

    return data


def authenticated(wrapped: callable) -> callable:
    """
    Decorator to check if the user is authenticated

    :param wrapped: Function to be decorated
    :return: Decorated function
    """
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = checkToken(request)

            if is_authenticated:
                async with request.app.ctx.pool.acquire() as connection:
                    data = await connection.fetchrow(
                        "SELECT username, account FROM users WHERE token = $1",
                        request.cookies.get("token"),
                    )

                if not data:
                    request.ctx.session["user"] = {
                        "username": "",
                        "authenticated": False
                    }

                    return redirect("/user/login")
                else:
                    request.ctx.session["user"] = {
                        "username": data["username"],
                        "account": data["account"],
                        "authenticated": True
                    }

                response = await f(request, *args, **kwargs)
                return response
            else:
                request.ctx.session["user"] = {
                    "username": "",
                    "authenticated": False
                }

                return redirect("/user/login")
        return decorated_function
    return decorator(wrapped)
