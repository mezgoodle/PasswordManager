from typing import Dict, List

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
        self, table: str, columns: str = "*", column: str = None, value: str = None
    ) -> List[dict]:
        """Method for getting all data from the table

        Args:
            table (str): name of the table
            columns (str, optional): names of the columns to select. Defaults to "*".
            column (str, optional): name of the column as condition. Defaults to None.
            value (str, optional): value of the column as condition. Defaults to None.

        Returns:
            List[dict]: list of the objects from the table
        """
        logger.info("Trying to getting data")
        try:
            if column:
                assert value is not None, "Value should be passed"
                data = (
                    self.client.table(table).select(columns).eq(column, value).execute()
                )
            else:
                data = self.client.table(table).select(columns).execute()
            return data.data
        except Exception as e:
            logger.error(e)

    def get_single(
        self, table: str, column: str, value: str, columns: str = "*"
    ) -> dict:
        """Method for getting single object from the table

        Args:
            table (str): name of the table
            column (str, optional): name of the column as condition.
            value (str, optional): value of the column as condition.
            columns (str, optional): names of the columns to select. Defaults to "*".

        Returns:
            dict: object from the table
        """
        logger.info("Trying to getting data")
        try:
            return self.get_all(table, columns, column, value)
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

    def sign_in(self, email: str, password: str) -> str:
        """Method for signing in in Supabase

        Args:
            email (str): email of the user
            password (str): password of the user

        Returns:
            str: access token
        """
        try:
            session = self.client.auth.sign_in(email=email, password=password)
            self.sign_out()
            return session.access_token
        except APIError:
            logger.error("Bad sign in")

    def sign_out(self) -> None:
        """Method for signing out from the Supabase

        Returns:
            None: nothing to return
        """
        return self.client.auth.sign_out()
