from sqlalchemy import Column, Integer, String
from database import Base

class ImageText(Base):
    __tablename__ = "imagetexts"
    
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    extracted_text = Column(String)
