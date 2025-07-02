import io
import json
import os

from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage
import requests


API_BASE = "https://recodeqr.com"
USER_AGENT = "RecodeQR-MCP/1.0"
HOST = "0.0.0.0"
PORT = os.environ.get("PORT", 8080)

# Create an MCP server
mcp = FastMCP(
    "RecodeQR",
    dependencies=["requests", "Pillow"],
    host=HOST,
    port=PORT,
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def generate_qr_code(content: str) -> Image:
    """Generate a QR code image from the given content."""
    data = json.dumps(
        {
            "destination": "text",
            "format": "png",
            "dynamic": False,
            "data": {"text": content},
        }
    )
    headers = {"content-type": "application/json", "user-agent": USER_AGENT}
    res = requests.post(f"{API_BASE}/api/generate", data=data, headers=headers)

    if 200 <= res.status_code <= 299:
        img = PILImage.open(io.BytesIO(res.content))
        return Image(data=img.tobytes(), format="png")
    elif 400 <= res.status_code <= 499:
        raise ValueError(res.json())
    else:
        raise Exception("Something went wrong with the request")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
