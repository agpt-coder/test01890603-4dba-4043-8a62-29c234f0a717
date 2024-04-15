from datetime import datetime

import httpx
from pydantic import BaseModel


class GetExchangeRateResponse(BaseModel):
    """
    Response model providing the current exchange rate from the specified base currency to the target currency, along with relevant metadata.
    """

    base_currency: str
    target_currency: str
    exchange_rate: float
    last_updated: str


async def get_exchange_rate(
    base_currency: str, target_currency: str
) -> GetExchangeRateResponse:
    """
    Retrieves current exchange rates for specified currencies.

    This function calls an external API to fetch real-time exchange rates between the specified base and target currencies.
    It constructs and returns a response model containing the exchange rate and relevant metadata.

    Args:
    base_currency (str): The ISO 4217 code of the base currency for which exchange rates are being requested.
    target_currency (str): The ISO 4217 code of the target currency against which the base currency's value is to be compared.

    Returns:
    GetExchangeRateResponse: Response model providing the current exchange rate from the specified base currency to the target currency, along with relevant metadata.

    Example:
    get_exchange_rate('USD', 'EUR')
    > GetExchangeRateResponse(base_currency='USD', target_currency='EUR', exchange_rate=0.84, last_updated='2023-10-04T00:00:00Z')
    """
    api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        response.raise_for_status()
        data = response.json()
        if target_currency not in data["rates"]:
            raise ValueError(
                f"The target currency '{target_currency}' is not available."
            )
        exchange_rate = data["rates"][target_currency]
        last_updated = data["time_last_updated"]
        formatted_last_updated = datetime.utcfromtimestamp(last_updated).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    return GetExchangeRateResponse(
        base_currency=base_currency,
        target_currency=target_currency,
        exchange_rate=exchange_rate,
        last_updated=formatted_last_updated,
    )
