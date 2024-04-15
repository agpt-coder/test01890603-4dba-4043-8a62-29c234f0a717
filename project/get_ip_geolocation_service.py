from typing import Optional

import httpx
import prisma
import prisma.models
from pydantic import BaseModel, ValidationError


class IPGeolocationResponseModel(BaseModel):
    """
    Provides the geolocation data for the given IP address, including the country, city, and if available, detailed location data like latitude and longitude.
    """

    country: str
    city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    isp: Optional[str] = None


async def get_ip_geolocation(ip_address: str) -> IPGeolocationResponseModel:
    """
    Provides geolocation data for the specified IP address.

    Args:
        ip_address (str): The IP address for which geolocation data is requested.

    Returns:
        IPGeolocationResponseModel: Provides the geolocation data for the given IP address,
        including the country, city, and if available, detailed location data like latitude and longitude.
    """
    api_url = f"https://ip-geolocation-api.example.com/{ip_address}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            data = response.json()
            await prisma.models.IPGeolocationRequest.prisma().create(
                data={"ip": ip_address}
            )
            geolocation_data = IPGeolocationResponseModel(
                country=data["country"],
                city=data["city"],
                latitude=data.get("latitude"),
                longitude=data.get("longitude"),
                isp=data.get("isp"),
            )
            return geolocation_data
    except (httpx.HTTPStatusError, ValidationError) as e:
        raise ValueError(f"Error fetching or parsing geolocation data: {e}")
