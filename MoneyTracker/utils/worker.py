import os

from .LCLPy import LCLClient
from ..utils.logger import Logger
from asyncpg import Pool, Connection
from dotenv import load_dotenv
from datetime import datetime


load_dotenv(dotenv_path='./.env')


class Worker:
    def __init__(self, pool: Pool, logger: Logger):
        self.pool = pool
        self.logger = logger


    def getDate(self, date: str) -> datetime:
        """
        Convertit une date au format ISO 8601 en objet datetime
        
        :param date: La date au format ISO 8601
        :return: L'objet datetime correspondant à la date
        """
        try:
            return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            try:
                return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f+0000")
            except ValueError:
                return None


    async def run(self):
        """
        Fonction principale du worker
        """
        # Pour chaque profil, récupération des transactions
        for profile in os.listdir("./profiles"):
            if profile == "example":
                continue

            # Connexion au compte LCL
            client = LCLClient(f"./profiles/{profile}/.env")


            # Insersion de l'utilisateur dans la base de données
            self.logger.info("Insertion de l'utilisateur dans la base de données...")

            async with self.pool.acquire() as connection:
                connection: Connection
                await connection.execute(
                    """
                        INSERT INTO public.accounts (
                            id,
                            username
                        ) VALUES (
                            $1, $2
                        ) ON CONFLICT (id) DO NOTHING;
                    """,
                    int(client.account_id),
                    profile.title()
                )


            # Mise à jour du solde de l'utilisateur
            self.logger.info("Mise à jour du solde de l'utilisateur...")

            balance = await client.getBalance()

            async with self.pool.acquire() as connection:
                connection: Connection
                await connection.execute(
                    """
                        UPDATE public.accounts SET balance = $1 WHERE id = $2;
                    """,
                    balance,
                    int(client.account_id)
                )

            self.logger.info("Solde mis à jour !")


            # Récupération des transactions
            self.logger.info("Récupération des transactions...")

            transactions = await client.getTransactions()

            self.logger.info("Transactions récupérées !")


            # Insertion des transactions dans la base de données
            self.logger.info("Insertion des transactions dans la base de données...")

            async with self.pool.acquire() as connection:
                connection: Connection
                for transaction in transactions:
                    # self.logger.info(f"Insertion de la transaction {transaction.id} ({transaction.label} - {transaction.amount} €)...")
                    await connection.execute(
                        """
                            INSERT INTO public.transactions (
                                id,
                                label,
                                booking_date_time,
                                is_accounted,
                                are_details_available,
                                amount,
                                amount_currency,
                                movement_code_type,
                                nature,
                                user_id
                            ) VALUES (
                                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
                            ) ON CONFLICT (id, label, booking_date_time, amount) DO UPDATE SET
                                id = $1,
                                label = $2,
                                booking_date_time = $3,
                                is_accounted = $4,
                                are_details_available = $5,
                                amount = $6,
                                amount_currency = $7,
                                movement_code_type = $8,
                                nature = $9;
                        """,
                        str(transaction.id),
                        transaction.label,
                        self.getDate(transaction.booking_date_time) if transaction.booking_date_time else None,
                        transaction.is_accounted,
                        transaction.are_details_available,
                        transaction.amount,
                        transaction.amount_currency,
                        transaction.movement_code_type,
                        transaction.nature,
                        int(client.account_id)
                    )

            self.logger.info("Transactions insérées dans la base de données !")

            self.logger.info(f"Fin du traitement pour le profil {profile} ({len(transactions)} transactions)")
