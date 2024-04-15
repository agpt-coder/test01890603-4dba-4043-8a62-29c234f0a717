from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GenerateQRCodeResponse(BaseModel):
    """
    The response object containing the generated QR code's URL and possibly some metadata related to the creation.
    """

    qrCodeUrl: str
    qrCodeId: Optional[str] = None


async def generate_qr_code(
    content: str,
    size: Optional[int] = None,
    encoding: Optional[str] = None,
    styleSettings: Optional[str] = None,
) -> GenerateQRCodeResponse:
    """
    Generates a QR code based on provided parameters and saves the request details to the database.

    Args:
        content (str): The content to be encoded into the QR code. This could be a URL, text message, or any other data.
        size (Optional[int]): The size of the generated QR code in pixels. Optional parameter.
        encoding (Optional[str]): The type of encoding to use for the QR code content. Optional parameter.
        styleSettings (Optional[str]): JSON string specifying any additional styling options for the QR code, such as color or border. Optional parameter.

    Returns:
        GenerateQRCodeResponse: The response object containing the generated QR code's URL and possibly some metadata related to the creation.

    Note: This implementation assumes a QR code generating API or utility is integrated that produces a URL pointing to the generated QR code image.

    """
    qr_code_url = "https://example.com/generated_qr_code.png"
    qr_code_request = await prisma.models.QRCodeRequest.prisma().create(
        data={
            "content": content,
            "encoding": encoding,
            "size": size,
            "styleSettings": styleSettings,
        }
    )
    return GenerateQRCodeResponse(qrCodeUrl=qr_code_url, qrCodeId=qr_code_request.id)
