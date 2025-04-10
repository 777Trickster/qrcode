from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import qrcode
import uuid
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate_qr")
def generate_qr(text: str = Query(..., description="Text to encode as QR code")):
    # Generate unique filename
    filename = f"{uuid.uuid4().hex}.png"
    filepath = f"./{filename}"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)

    return FileResponse(
        path=filepath,
        filename="qr_code.png",
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename=qr_code.png"},
    )
