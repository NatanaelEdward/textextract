from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import ImageText
from database import get_db
import pytesseract
from PIL import Image
import cv2
import numpy as np

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/imagetexts/")
async def create_image_text(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    pil_image = Image.fromarray(binary_image)

    extracted_text = pytesseract.image_to_string(pil_image)

    image_path = f"images/{file.filename}"
    cv2.imwrite(image_path, image)

    db_imagetext = ImageText(image_url=image_path, extracted_text=extracted_text)
    db.add(db_imagetext)
    db.commit()
    db.refresh(db_imagetext)
    return {"extracted_text": extracted_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
