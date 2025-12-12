from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import os
import uuid
from db.database import engine, SessionLocal, get_db
from db.models import File as FileModel
import db.models as models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="File Storage API", version="1.0.0")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "Welcome to File Storage API",
        "docs": "Visit http://localhost:8000/docs for API documentation"
    }

@app.post("/api/upload")
async def upload_files(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    """Upload one or more files and save to database"""
    uploaded_files = []
    
    try:
        for file in files:
            # Generate unique filename to avoid conflicts
            file_ext = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            # Read and save file
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Create database record
            db_file = FileModel(
                filename=unique_filename,
                original_filename=file.filename,
                file_path=file_path,
                file_size=file_size,
                file_type=file.content_type or "application/octet-stream",
            )
            
            db.add(db_file)
            db.commit()
            db.refresh(db_file)
            
            uploaded_files.append({
                "id": db_file.id,
                "name": db_file.original_filename,
                "size": db_file.file_size,
                "uploaded_at": db_file.uploaded_at.isoformat(),
            })
        
        return {
            "message": "Files uploaded successfully",
            "files": uploaded_files
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/files")
def list_files(db: Session = Depends(get_db)):
    """Get list of all uploaded files from database"""
    files = db.query(FileModel).all()
    
    return {
        "total": len(files),
        "files": [
            {
                "id": f.id,
                "name": f.original_filename,
                "size": f.file_size,
                "uploaded_at": f.uploaded_at.isoformat(),
                "type": f.file_type,
            }
            for f in files
        ]
    }

@app.get("/api/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    """Download a file by ID"""
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(db_file.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return FileResponse(
        path=db_file.file_path,
        filename=db_file.original_filename,
        media_type=db_file.file_type
    )

@app.delete("/api/files/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    """Delete a file by ID"""
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete from filesystem
    if os.path.exists(db_file.file_path):
        os.remove(db_file.file_path)
    
    # Delete from database
    db.delete(db_file)
    db.commit()
    
    return {
        "message": "File deleted successfully",
        "filename": db_file.original_filename
    }