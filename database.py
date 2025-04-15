import logging
from enum import Enum
from typing import Dict, List, Optional

from sqlalchemy import TIMESTAMP, BigInteger, Boolean, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import (
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    Text,
    create_engine,
    delete,
    insert,
    or_,
    update,
)
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import func

from config import config
from logging_conf import configure_logging

# Configuración de logging
configure_logging()
logger = logging.getLogger("chatbot.database")


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    BET = "bet"
    WIN = "win"
    TRANSFER_OUT = "transfer_out"
    TRANSFER_IN = "transfer_in"


class BetStatus(Enum):
    PENDING = "pending"
    CANCEL = "cancel"
    WIN = "win"
    LOSE = "lose"


class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.metadata = MetaData()
        self.engine = create_engine(database_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

        # Definición de tablas
        self.users = Table("users", self.metadata, *self._get_user_columns())

        self.sports = Table("sports", self.metadata, *self._get_sport_columns())

        self.competitions = Table(
            "competitions", self.metadata, *self._get_competition_columns()
        )

        self.matches = Table("matches", self.metadata, *self._get_match_columns())

        self.bet_types = Table(
            "bet_types", self.metadata, *self._get_bet_type_columns()
        )

        self.match_bet_options = Table(
            "match_bet_options", self.metadata, *self._get_match_bet_option_columns()
        )

        self.bets = Table("bets", self.metadata, *self._get_bet_columns())

        self.transactions = Table(
            "transactions", self.metadata, *self._get_transaction_columns()
        )

        self.transfers = Table(
            "transfers", self.metadata, *self._get_transfer_columns()
        )

        self.metadata.create_all(self.engine)

    def connect(self):
        self.session = self.Session()
        logger.info("Connected to database")

    def disconnect(self):
        if hasattr(self, "session"):
            self.session.close()
            logger.info("Disconnected from database")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    # Métodos auxiliares para definir columnas
    def _get_user_columns(self):
        return [
            Column("user_id", BigInteger, primary_key=True),
            Column("username", String(100)),
            Column("first_name", String(100), nullable=False),
            Column("last_name", String(100)),
            Column("balance", Numeric(15, 2), nullable=False, server_default="0.00"),
            Column(
                "registration_date",
                TIMESTAMP,
                nullable=False,
                server_default=func.now(),
            ),
            Column("is_active", Boolean, nullable=False, server_default="true"),
            Column("is_admin", Boolean, nullable=False, server_default="false"),
        ]

    def _get_sport_columns(self):
        return [
            Column("sport_id", Integer, primary_key=True),
            Column("name", String(100), nullable=False),
            Column("is_active", Boolean, nullable=False, server_default="true"),
        ]

    def _get_competition_columns(self):
        return [
            Column("competition_id", Integer, primary_key=True),
            Column(
                "sport_id",
                Integer,
                ForeignKey("sports.sport_id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column("name", String(100), nullable=False),
            Column("country", String(100)),
            Column("is_active", Boolean, nullable=False, server_default="true"),
        ]

    def _get_match_columns(self):
        return [
            Column("match_id", Integer, primary_key=True),
            Column(
                "competition_id",
                Integer,
                ForeignKey("competitions.competition_id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column("team_home", String(100), nullable=False),
            Column("team_away", String(100), nullable=False),
            Column("match_date", TIMESTAMP, nullable=False),
            Column("status", String(20), nullable=False, server_default="pending"),
            Column("result", String(20)),
            Column("created_at", TIMESTAMP, nullable=False, server_default=func.now()),
            Column("updated_at", TIMESTAMP),
        ]

    def _get_bet_type_columns(self):
        return [
            Column("bet_type_id", Integer, primary_key=True),
            Column("name", String(100), nullable=False),
            Column("description", Text),
            Column("is_active", Boolean, nullable=False, server_default="true"),
        ]

    def _get_match_bet_option_columns(self):
        return [
            Column("option_id", Integer, primary_key=True),
            Column(
                "match_id",
                Integer,
                ForeignKey("matches.match_id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column(
                "bet_type_id",
                Integer,
                ForeignKey("bet_types.bet_type_id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column("prediction", String(100), nullable=False),
            Column("odds", Numeric(5, 2), nullable=False),
            Column("is_active", Boolean, nullable=False, server_default="true"),
        ]

    def _get_bet_columns(self):
        return [
            Column("bet_id", Integer, primary_key=True),
            Column(
                "user_id",
                BigInteger,
                ForeignKey("users.user_id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column(
                "option_id",
                Integer,
                ForeignKey("match_bet_options.option_id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column("amount", Numeric(10, 2), nullable=False),
            Column("potential_win", Numeric(10, 2), nullable=False),
            Column("status", SQLAlchemyEnum(BetStatus), nullable=False, server_default="PENDING"),
            Column("created_at", TIMESTAMP, nullable=False, server_default=func.now()),
            Column("settled_at", TIMESTAMP),
        ]

    def _get_transaction_columns(self):
        return [
            Column("transaction_id", Integer, primary_key=True),
            Column(
                "user_id",
                BigInteger,
                ForeignKey("users.user_id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column("amount", Numeric(10, 2), nullable=False),
            Column("type", SQLAlchemyEnum(TransactionType), nullable=False),
            Column("status", String(20), nullable=False, server_default="pending"),
            Column("description", Text),
            Column(
                "admin_id", BigInteger, ForeignKey("users.user_id", ondelete="CASCADE")
            ),
            Column("proof_image", String(255)),
            Column("created_at", TIMESTAMP, nullable=False, server_default=func.now()),
            Column("processed_at", TIMESTAMP),
        ]

    def _get_transfer_columns(self):
        return [
            Column("transfer_id", Integer, primary_key=True),
            Column(
                "sender_id",
                BigInteger,
                ForeignKey("users.user_id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column(
                "receiver_id",
                BigInteger,
                ForeignKey("users.user_id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column("amount", Numeric(10, 2), nullable=False),
            Column("created_at", TIMESTAMP, nullable=False, server_default=func.now()),
        ]

    # CRUD para Users
    def create_user(self, user_data: Dict) -> int:
        query = insert(self.users).values(user_data)
        result = self.session.execute(query)
        self.session.commit()
        return result.inserted_primary_key[0]

    def get_user(self, user_id: int) -> Optional[Dict]:
        logger.debug("get_user")
        query = self.users.select().where(self.users.c.user_id == user_id)
        result = self.session.execute(query)
        return result.fetchone()._asdict() if result.rowcount else None

    def update_user(self, user_id: int, user_data: Dict) -> bool:
        logger.debug("update_user")
        query = (
            update(self.users).where(self.users.c.user_id == user_id).values(user_data)
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    def delete_user(self, user_id: int) -> bool:
        logger.debug("delete_user")
        query = delete(self.users).where(self.users.c.user_id == user_id)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    def update_user_balance(self, user_id: int, amount: float) -> bool:
        logger.debug("update_user_balance")
        query = (
            update(self.users)
            .where(self.users.c.user_id == user_id)
            .values(balance=self.users.c.balance + amount)
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    # CRUD para Sports
    def create_sport(self, sport_data: Dict) -> int:
        logger.debug("create_sport")
        query = insert(self.sports).values(sport_data)
        result = self.session.execute(query)
        self.session.commit()
        return result.inserted_primary_key[0]

    def get_sport(self, sport_id: int) -> Optional[Dict]:
        logger.debug("get_sport")
        query = self.sports.select().where(self.sports.c.sport_id == sport_id)
        result = self.session.execute(query)
        return result.fetchone()._asdict() if result.rowcount else None

    def get_all_active_sports(self) -> List[Dict]:
        logger.debug("get_all_active_sports")
        query = self.sports.select().where(self.sports.c.is_active)
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def update_sport(self, sport_id: int, sport_data: Dict) -> bool:
        logger.debug("update_sport")
        query = (
            update(self.sports)
            .where(self.sports.c.sport_id == sport_id)
            .values(sport_data)
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    def delete_sport(self, sport_id: int) -> bool:
        logger.debug("delete_sport")
        query = delete(self.sports).where(self.sports.c.sport_id == sport_id)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    # CRUD para Competitions
    def create_competition(self, competition_data: Dict) -> int:
        logger.debug("create_competition")
        query = insert(self.competitions).values(competition_data)
        result = self.session.execute(query)
        self.session.commit()
        return result.inserted_primary_key[0]

    def get_competition(self, competition_id: int) -> Optional[Dict]:
        logger.debug("get_competition")
        query = self.competitions.select().where(
            self.competitions.c.competition_id == competition_id
        )
        result = self.session.execute(query)
        return result.fetchone()._asdict() if result.rowcount else None

    def get_competitions_by_sport(self, sport_id: int) -> List[Dict]:
        logger.debug("get_competitions_by_sport")
        query = self.competitions.select().where(
            self.competitions.c.sport_id == sport_id
        )
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def update_competition(self, competition_id: int, competition_data: Dict) -> bool:
        logger.debug("update_competition")
        query = (
            update(self.competitions)
            .where(self.competitions.c.competition_id == competition_id)
            .values(competition_data)
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    def delete_competition(self, competition_id: int) -> bool:
        logger.debug("delete_competition")
        query = delete(self.competitions).where(
            self.competitions.c.competition_id == competition_id
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    # CRUD para Matches
    def create_match(self, match_data: Dict) -> int:
        logger.debug("create_match")
        query = insert(self.matches).values(match_data)
        result = self.session.execute(query)
        self.session.commit()
        return result.inserted_primary_key[0]

    def get_upcoming_matches(self, limit: int = 10) -> List[Dict]:
        logger.debug("get_upcoming_matches")
        query = (
            self.matches.select()
            .where(self.matches.c.status == "pending")
            .order_by(self.matches.c.match_date)
            .limit(limit)
        )
        logger.debug(query)
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def update_match(self, match_id: int, match_data: Dict) -> bool:
        logger.debug("update_match")
        match_data["updated_at"] = func.now()
        query = (
            update(self.matches)
            .where(self.matches.c.match_id == match_id)
            .values(match_data)
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    def get_match(self, match_id: int) -> Optional[Dict]:
        logger.debug("get_match")
        query = self.matches.select().where(self.matches.c.match_id == match_id)
        result = self.session.execute(query)
        return result.fetchone()._asdict() if result.rowcount else None

    def get_matches_by_competition(
        self, competition_id: int, limit: int = 50
    ) -> List[Dict]:
        logger.debug("get_matches_by_competition")
        query = (
            self.matches.select()
            .where(self.matches.c.competition_id == competition_id)
            .order_by(self.matches.c.match_date)
            .limit(limit)
        )
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def set_match_result(self, match_id: int, result: str) -> bool:
        logger.debug("set_match_result")
        query = (
            update(self.matches)
            .where(self.matches.c.match_id == match_id)
            .values(result=result, status="finished", updated_at=func.now())
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    def delete_match(self, match_id: int) -> bool:
        logger.debug("delete_match")
        query = delete(self.matches).where(self.matches.c.match_id == match_id)
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    # CRUD para BetTypes
    def create_bet_type(self, bet_type_data: Dict) -> int:
        logger.debug("create_bet_type")
        query = insert(self.bet_types).values(bet_type_data)
        result = self.session.execute(query)
        self.session.commit()
        return result.inserted_primary_key[0]

    def get_all_bet_types(self, active_only: bool = True) -> List[Dict]:
        logger.debug("get_all_bet_types")
        query = self.bet_types.select()
        if active_only:
            query = query.where(self.bet_types.c.is_active)
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def update_bet_type(self, bet_type_id: int, bet_type_data: Dict) -> bool:
        logger.debug("update_bet_type")
        query = (
            update(self.bet_types)
            .where(self.bet_types.c.bet_type_id == bet_type_id)
            .values(bet_type_data)
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    def delete_bet_type(self, bet_type_id: int) -> bool:
        logger.debug("delete_bet_type")
        query = delete(self.bet_types).where(
            self.bet_types.c.bet_type_id == bet_type_id
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    # CRUD para MatchBetOptions
    def create_match_bet_option(self, option_data: Dict) -> int:
        logger.debug("create_match_bet_option")
        query = insert(self.match_bet_options).values(option_data)
        result = self.session.execute(query)
        self.session.commit()
        return result.inserted_primary_key[0]

    def get_bet_options_for_match(
        self, match_id: int, active_only: bool = True
    ) -> List[Dict]:
        logger.debug("get_bet_option_for_match")
        query = self.match_bet_options.select().where(
            self.match_bet_options.c.match_id == match_id
        )
        if active_only:
            query = query.where(self.match_bet_options.c.is_active)
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def update_bet_option(self, option_id: int, bet_option_data: Dict) -> bool:
        logger.debug("update_bet_option")
        query = (
            update(self.match_bet_options)
            .where(self.match_bet_options.c.option_id == option_id)
            .values(bet_option_data)
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    def delete_match_bet_option(self, option_id: int) -> bool:
        logger.debug("delete_match_bet_option")
        query = delete(self.match_bet_options).where(
            self.match_bet_options.c.option_id == option_id
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    # CRUD para Transactions
    def create_transaction(self, transaction_data: Dict) -> int:
        logger.debug("create_transaction")
        query = insert(self.transactions).values(transaction_data)
        result = self.session.execute(query)
        self.session.commit()
        return result.inserted_primary_key[0]

    def approve_transaction(self, transaction_id: int, admin_id: int) -> bool:
        logger.debug("approve_transaction")
        try:
            # 1. Obtener la transacción
            query = self.transactions.select().where(
                self.transactions.c.transaction_id == transaction_id
            )
            transaction_result = self.session.execute(query)
            transaction = transaction_result.fetchone()

            if not transaction or transaction["status"] != "pending":
                return False

            # 2. Actualizar estado
            update_query = (
                update(self.transactions)
                .where(self.transactions.c.transaction_id == transaction_id)
                .values(status="approved", admin_id=admin_id, processed_at=func.now())
            )
            self.session.execute(update_query)

            # 3. Si es depósito, acreditar saldo. Si es extracción retirar
            if transaction["type"] == "deposit":
                self.update_user_balance(transaction["user_id"], transaction["amount"])
            elif transaction["type"] == "withdrawal":
                user = self.get_user(transaction["user_id"])
                if user["balance"] < transaction["amount"]:
                    logger.warning(
                        f"El usuario {user['name']} no tiene suficiente saldo para realizar la extracción. Balance: {user['balance']} Cantidad solicitada: {transaction['amount']}"
                    )
                    return False

                self.update_user_balance(transaction["user_id"], -transaction["amount"])

            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error approving transaction: {e}")
            return False

    def get_transaction(self, transaction_id: int) -> Optional[Dict]:
        logger.debug("get_transaction")
        query = self.transactions.select().where(
            self.transactions.c.transaction_id == transaction_id
        )
        result = self.session.execute(query)
        return result.fetchone()._asdict() if result.rowcount else None

    def get_user_transactions(self, user_id: int, limit: int = 50) -> List[Dict]:
        logger.debug("get_user_transactions")
        query = (
            self.transactions.select()
            .where(self.transactions.c.user_id == user_id)
            .order_by(self.transactions.c.created_at.desc())
            .limit(limit)
        )
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def reject_transaction(self, transaction_id: int, admin_id: int) -> bool:
        logger.debug("reject_transaction")
        query = (
            update(self.transactions)
            .where(self.transactions.c.transaction_id == transaction_id)
            .values(status="rejected", admin_id=admin_id, processed_at=func.now())
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount > 0

    # CRUD para Transfers
    def create_transfer(self, transfer_data: Dict) -> int:
        logger.debug("create_transfer")
        query = insert(self.transfers).values(transfer_data)
        result = self.session.execute(query)
        self.session.commit()
        return result.inserted_primary_key[0]

    def get_transfer(self, transfer_id: int) -> Optional[Dict]:
        logger.debug("get_transfer")
        query = self.transfers.select().where(
            self.transfers.c.transfer_id == transfer_id
        )
        result = self.session.execute(query)
        return result.fetchone()._asdict() if result.rowcount else None

    def get_user_transfers(
        self, user_id: int, direction: str = "all", limit: int = 50
    ) -> List[Dict]:
        logger.debug("get_user_transfer")
        query = self.transfers.select()

        if direction == "sent":
            query = query.where(self.transfers.c.sender_id == user_id)
        elif direction == "received":
            query = query.where(self.transfers.c.receiver_id == user_id)
        else:
            query = query.where(
                or_(
                    self.transfers.c.sender_id == user_id,
                    self.transfers.c.receiver_id == user_id,
                )
            )

        query = query.order_by(self.transfers.c.created_at.desc()).limit(limit)
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    # CRUD para Bets
    def create_bet(self, bet_data: Dict) -> int:
        logger.debug("create_bet")
        try:
            # 1. Crear la apuesta
            query = insert(self.bets).values(bet_data)
            result = self.session.execute(query)
            bet_id = result.inserted_primary_key[0]

            # 2. Descontar el saldo del usuario
            user_id = bet_data["user_id"]
            amount = bet_data["amount"]
            user = self.get_user(user_id)
            if user["balance"] < amount:
                logger.warning(
                    f"El usuario {user['name']} no tiene suficiente saldo para realizar la operación. Balance: {user['balance']} Solicitud: {amount}"
                )
                return False

            self.update_user_balance(user_id, -amount)

            # 3. Registrar la transacción
            transaction_data = {
                "user_id": user_id,
                "amount": amount,
                "type": "bet",
                "status": "completed",
                "description": f"Apuesta #{bet_id}",
            }
            self.create_transaction(transaction_data)

            self.session.commit()
            return bet_id
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating bet: {e}")
            return False

    def settle_bet(self, bet_id: int, won: bool) -> bool:
        logger.debug("settle_bet")
        try:
            # 1. Obtener información de la apuesta
            bet_query = self.bets.select().where(self.bets.c.bet_id == bet_id)
            bet_result = self.session.execute(bet_query)
            bet = bet_result.fetchone()

            if not bet or bet["status"] != "pending":
                return False

            # 2. Actualizar estado de la apuesta
            update_bet_query = (
                update(self.bets)
                .where(self.bets.c.bet_id == bet_id)
                .values(status="won" if won else "lost", settled_at=func.now())
            )
            self.session.execute(update_bet_query)

            # 3. Si ganó, acreditar el premio
            if won:
                self.update_user_balance(bet["user_id"], bet["potential_win"])

                # Registrar transacción
                transaction_data = {
                    "user_id": bet["user_id"],
                    "amount": bet["potential_win"],
                    "type": "win",
                    "status": "completed",
                    "description": f"Ganancia apuesta #{bet_id}",
                }
                self.create_transaction(transaction_data)

            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error settling bet: {e}")
            return False

    # Métodos adicionales para operaciones complejas
    def get_user_bets(self, user_id: int, status: str = None) -> List[Dict]:
        logger.debug("get_user_bets")
        query = self.bets.select().where(self.bets.c.user_id == user_id)
        if status:
            query = query.where(self.bets.c.status == status)
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def get_pending_transactions(self) -> List[Dict]:
        logger.debug("get_pending_transactions")
        query = (
            self.transactions.select()
            .where(self.transactions.c.status == "pending")
            .order_by(self.transactions.c.created_at)
        )
        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def transfer_balance(self, sender_id: int, receiver_id: int, amount: float) -> bool:
        logger.debug("transfer_balance")
        try:
            # 1. Verificar saldo del emisor
            sender = self.get_user(sender_id)
            if not sender or sender["balance"] < amount:
                logger.warning(
                    f"El usuario {sender['name']} no tiene suficiente saldo para realizar la operación. Balance: {sender['balance']} Cantidad solicitada: {amount}"
                )
                return False

            # 2. Actualizar saldos
            self.update_user_balance(sender_id, -amount)
            self.update_user_balance(receiver_id, amount)

            # 3. Registrar transferencia
            transfer_data = {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "amount": amount,
            }
            self.create_transfer(transfer_data)

            # 4. Registrar transacciones
            sender_transaction = {
                "user_id": sender_id,
                "amount": amount,
                "type": "transfer_out",
                "status": "completed",
                "description": f"Transferencia a usuario #{receiver_id}",
            }
            self.create_transaction(sender_transaction)

            receiver_transaction = {
                "user_id": receiver_id,
                "amount": amount,
                "type": "transfer_in",
                "status": "completed",
                "description": f"Transferencia de usuario #{sender_id}",
            }
            self.create_transaction(receiver_transaction)

            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error transferring balance: {e}")
            return False


db = DatabaseManager(config.DATABASE_URL)
