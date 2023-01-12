from typing import Dict

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
        logger.info(f'Inserting data into "{table}" table')
        data = self.client.table(table).insert(values).execute()
        return len(data.data) > 0
