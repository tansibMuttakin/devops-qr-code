from typing import Union, Optional
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import boto3
import os
from io import BytesIO
from fastapi import FastAPI

# Loading environment variabes
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

#Allowing origins for local testing
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# AWS S3 configuration
s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

bucket_name = os.getenv('BUCKET_NAME')

@app.get("/")
async def read_root():
    return ("This is a basic fastapi application.")

@app.post("/generate-qr")
async def generate_qr(url: str)-> Union[dict,str]:
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR Code to BytesIO object
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Generate file name for s3
    file_name = f"qr_codes/{url.split('//')[-1]}.png"

    try:
        # # Upload QR Code to S3
        # s3.put_object(
        #     Bucket = bucket_name,
        #     Key = file_name,
        #     Body = img_byte_arr,
        #     ContentType = 'image/png',
        #     ACL = 'public-read'
        # )

        # # Generate s3 URL
        # s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        return {
            "qr_code_url": "s3_url"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))