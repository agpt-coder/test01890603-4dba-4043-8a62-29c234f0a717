import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.authenticate_user_service
import project.generate_qr_code_service
import project.get_exchange_rate_service
import project.get_ip_geolocation_service
import project.submit_feedback_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="test",
    lifespan=lifespan,
    description="The Multi-Purpose API Toolkit is a comprehensive suite of APIs designed for developers to streamline various tasks without the need for integrating multiple third-party services. It includes APIs for QR Code Generation, Currency Exchange Rate, IP Geolocation, Image Resizing, Password Strength Checking, Text-to-Speech, Barcode Generation, Email Validation, Time Zone Conversion, URL Preview, PDF Watermarking, and converting RSS Feeds to JSON. This all-in-one toolkit aims to provide simplicity and ease of use for common development needs.",
)


@app.post(
    "/qr/generate",
    response_model=project.generate_qr_code_service.GenerateQRCodeResponse,
)
async def api_post_generate_qr_code(
    content: str,
    size: Optional[int],
    encoding: Optional[str],
    styleSettings: Optional[str],
) -> project.generate_qr_code_service.GenerateQRCodeResponse | Response:
    """
    Generates a QR code based on provided parameters.
    """
    try:
        res = await project.generate_qr_code_service.generate_qr_code(
            content, size, encoding, styleSettings
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback/submit",
    response_model=project.submit_feedback_service.SubmitFeedbackResponse,
)
async def api_post_submit_feedback(
    user_id: str, feedback: str
) -> project.submit_feedback_service.SubmitFeedbackResponse | Response:
    """
    Allows users to submit feedback about the toolkit.
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(user_id, feedback)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/ip/geolocate",
    response_model=project.get_ip_geolocation_service.IPGeolocationResponseModel,
)
async def api_post_get_ip_geolocation(
    ip_address: str,
) -> project.get_ip_geolocation_service.IPGeolocationResponseModel | Response:
    """
    Provides geolocation data for the specified IP address.
    """
    try:
        res = await project.get_ip_geolocation_service.get_ip_geolocation(ip_address)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/currency/exchange",
    response_model=project.get_exchange_rate_service.GetExchangeRateResponse,
)
async def api_get_get_exchange_rate(
    base_currency: str, target_currency: str
) -> project.get_exchange_rate_service.GetExchangeRateResponse | Response:
    """
    Retrieves current exchange rates for specified currencies.
    """
    try:
        res = await project.get_exchange_rate_service.get_exchange_rate(
            base_currency, target_currency
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/login",
    response_model=project.authenticate_user_service.AuthenticateUserResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserResponse | Response:
    """
    Authenticates a user and provides an access token.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
