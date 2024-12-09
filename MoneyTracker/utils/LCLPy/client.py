import aiohttp

from . import __baseURL__, __headers__
from .objects import Transactions
from os import environ
from dotenv import load_dotenv
from datetime import datetime


class LCLClient:
    """
    LCL Reverse-Engineering Client
    """
    def __init__(self, dotenv_path: str) -> None:
        load_dotenv(dotenv_path=dotenv_path)
        self.account_id = environ["ACCOUNT_IDENTIFIER"]

        self.account_data = None


    async def login(self):
        BODY = {
            "identifier": environ["ACCOUNT_IDENTIFIER"],
            "encryptedIdentifier": False,
            "keypad": environ["KEYPAD"],
            "callingUrl": "/connexion",
            "sessionId": environ["SESSION_ID"],
            "clientTimestamp": int(datetime.now().timestamp()),
        }

        async with aiohttp.ClientSession(headers=__headers__) as session:
            async with session.post(f"{__baseURL__}/login", json=BODY) as response:
                self.account_data = await response.json()


    async def getBalance(self):
        if self.account_data is None:
            await self.login()

        headers = {
            **__headers__,
            "X-Authorization": f"Bearer {self.account_data['accessToken']}",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{__baseURL__}/user/accounts?type=current&contract_id={environ['CONTRACT_ID']}&is_eligible_for_identity=false&include_aggregate_account=false") as response:
                data = await response.json()

        account_data = next((account for account in data["accounts"] if account["internal_id"] == environ["ACCOUNT_ID"]), None)
        if account_data is None:
            balance = -1
        else:
            balance = account_data["amount"]["value"]

        return balance


    async def getTransactions(self):
        if self.account_data is None:
            await self.login()

        headers = {
            **__headers__,
            "X-Authorization": f"Bearer {self.account_data['accessToken']}",
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{__baseURL__}/user/accounts/{environ['ACCOUNT_ID']}/transactions?contract_id={environ['CONTRACT_ID']}&range=0-500") as response:
                data = await response.json()

        return Transactions(data)
