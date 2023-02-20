from typing import Dict, List, Tuple

from aiogram.fsm.context import FSMContext
from gotrue.exceptions import APIError
from loguru import logger
from supabase import Client, create_client

from tgbot.config import config


class SUPABASE_CLIENT:
    def __init__(
        self,
        url: str = config.SUPABASE_URL.get_secret_value(),
        key: str = config.SUPABASE_KEY.get_secret_value(),
    ) -> None:
        """Function for getting the supabase client

        Args:
            url (str, optional): a RESTful endpoint for querying and managing your database. Defaults to config.SUPABASE_URL.get_secret_value().
            key (str, optional): this key has the ability to bypass Row Level Security. Never share it publicly. Defaults to config.SUPABASE_KEY.get_secret_value().
        """
        self.client: Client = create_client(url, key)

    def insert(self, table: str, values: Dict[str, str]) -> bool:
        """Method for inserting data into the base

        Args:
            table (str): name of the table
            values (Dict[str, str]): values, where key is row name and value is row value

        Returns:
            bool: if inserted data length more than zero
        """
        logger.info(f'Trying to insert data into "{table}" table')
        try:
            data = self.client.table(table).insert(values).execute()
            return len(data.data) > 0
        except Exception as e:
            logger.error(e)

    def get_all(
        self, table: str, columns: str = "*", conditions: dict = None
    ) -> Tuple[List[dict], int]:
        """Method for getting all data from the table

        Args:
            table (str): name of the table
            columns (str, optional): names of the columns to select. Defaults to "*".
            conditions (dict, optional): name of the column as condition. Defaults to None.

        Returns:
            Tuple[List[dict], int]: list of the objects and number of rows
        """
        logger.info("Trying to getting data")
        try:
            data = self.client.table(table).select(columns, count="exact").order("name")
            if conditions:
                for column, value in conditions.items():
                    data = data.eq(column, value)
            data = data.execute()
            return data.data, data.count
        except Exception as e:
            logger.error(e)

    def get_single(
        self, table: str, column: str, value: str, columns: str = "*"
    ) -> dict:
        """Method for getting single object from the table

        Args:
            table (str): name of the table
            column (str): name of the column as condition.
            value (str): value of the column as condition.
            columns (str, optional): names of the columns to select. Defaults to "*".

        Returns:
            dict: object from the table
        """
        logger.info("Trying to getting data")
        try:
            return self.get_all(table, columns, {column: value})[0][0]
        except Exception as e:
            logger.error(e)

    def update(
        self, table: str, columns: Dict[str, str], column: str, value: str
    ) -> List[dict]:
        """Method for updating objects in the table

        Args:
            table (str): name of the table
            columns (Dict[str, str]): dictionary with columns to changed to values
            column (str): name of the column as condition
            value (str): value of the column as condition

        Returns:
            List[dict]: list of the objects which were updated
        """
        logger.info("Trying to update the data")
        try:
            data = self.client.table(table).update(columns).eq(column, value).execute()
            print(data.data)
            return data
        except Exception as e:
            logger.error(e)

    def delete(self, table: str, column: str, value: str) -> List[dict]:
        """Method for deleting data in the table

        Args:
            table (str): name of the table
            column (str): name of the column as condition
            value (str): value of the column as condition

        Returns:
            List[dict]: list of the deleted objects
        """
        logger.info("Trying to delete the data")
        try:
            data = self.client.table(table).delete().eq(column, value).execute()
            return data.data
        except Exception as e:
            logger.error(e)

    def sign_up(self, email: str, password: str) -> dict:
        """Method for signing up in the Supabase

        Args:
            email (str): email of the user
            password (str): password of the user

        Returns:
            dict: dict representation of the user model
        """
        logger.info("Trying to sign up")
        try:
            user = self.client.auth.sign_up(email=email, password=password)
            return user.dict()
        except Exception as e:
            logger.error(e)

    async def sign_in(self, email: str, password: str) -> str:
        """Method for signing in in Supabase

        Args:
            email (str): email of the user
            password (str): password of the user

        Returns:
            str: access token
        """
        try:
            session = self.client.auth.sign_in(email=email, password=password)
            self.client.auth.sign_out()
            return session.access_token
        except APIError:
            logger.error("Bad sign in")

    async def sign_out(self, state: FSMContext) -> None:
        """Method for signing out from the bot app

        Args:
            state (FSMContext): state from aiogram

        Returns:
            None: nothing to return
        """
        user_data = await state.get_data()
        try:
            _ = user_data["token"]
            await state.clear()
            return
        except KeyError:
            pass
