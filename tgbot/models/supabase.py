from supabase import Client, create_client

from tgbot.config import config


def get_client(
    url: str = config.SUPABASE_URL.get_secret_value(),
    key: str = config.SUPABASE_KEY.get_secret_value(),
) -> Client:
    """Function for getting the supabase client

    Args:
        url (str, optional): a RESTful endpoint for querying and managing your database. Defaults to config.SUPABASE_URL.get_secret_value().
        key (str, optional): this key has the ability to bypass Row Level Security. Never share it publicly.. Defaults to config.SUPABASE_KEY.get_secret_value().

    Returns:
        Client: the supabase client to interface with your database.
    """
    return create_client(url, key)
