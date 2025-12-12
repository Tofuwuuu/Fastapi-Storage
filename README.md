# Google Drive-Like File Storage System

A self-hosted, open-source file management system inspired by Google Drive. Upload, organize, and manage your files with a modern web interface. Built with FastAPI for a robust backend and React + Vite for a responsive frontend.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Frontend-Backend Communication](#frontend-backend-communication)
- [Future Improvements](#future-improvements)
- [License](#license)

## 🎯 Overview

This project provides a lightweight, self-hosted alternative to cloud storage services. It allows users to store and manage files locally with an intuitive web-based interface. The system is designed to be easy to deploy, customize, and extend for personal or organizational use.

Perfect for:
- Personal file storage
- Team collaboration on internal networks
- Backing up important documents
- Learning full-stack web development

## ✨ Features

- **File Upload**: Drag-and-drop and click-to-upload functionality
- **File Management**: View, organize, and manage stored files
- **File Download**: Quick and easy file retrieval
- **File Listing**: Browse all stored files with metadata (name, size, date)
- **Responsive UI**: Works on desktop and mobile devices
- **RESTful API**: Clean, documented API endpoints for file operations
- **Local Storage**: Files stored securely on your server
- **Simple Deployment**: Run locally or on a VPS

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Modern Python web framework with auto-generated API docs |
| **Python 3.8+** | Backend programming language |
| **Uvicorn** | ASGI server for running FastAPI applications |
| **Pydantic** | Data validation and settings management |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **React 18** | UI component library |
| **Vite** | Fast build tool and dev server |
| **TypeScript** | Type-safe JavaScript |
| **CSS3** | Styling and responsive design |

## 📦 Requirements

### Backend
- Python 3.8 or higher
- pip (Python package installer)

### Frontend
- Node.js 16.0 or higher
- npm or yarn (Node package manager)

### System
- 50MB free disk space (minimum)
- 512MB RAM (minimum)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fastapi-storage.git
cd fastapi-storage
```

### 2. Backend Setup

#### Create and activate a Python virtual environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install backend dependencies

```bash
pip install fastapi uvicorn python-multipart
```

Or install from a `requirements.txt` (if available):
```bash
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## 📖 Usage

### Running the Backend

With your virtual environment activated:

```bash
python main.py
```

Or explicitly using Uvicorn:

```bash
uvicorn main:app --reload
```

The backend will start on `http://localhost:8000`

**API Documentation** (auto-generated):
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Running the Frontend

In a new terminal, from the `frontend` directory:

```bash
npm run dev
```

The frontend will start on `http://localhost:5173` (or the next available port)

### Production Deployment

**Backend:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
npm run build
npm run preview
```

## 🔌 API Endpoints

### Upload File

**POST** `/api/upload`

Upload a single or multiple files.

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "files=@document.pdf" \
  -F "files=@image.png"
```

**Response:**
```json
{
  "message": "Files uploaded successfully",
  "files": ["document.pdf", "image.png"]
}
```

### List Files

**GET** `/api/files`

Retrieve a list of all stored files.

```bash
curl "http://localhost:8000/api/files"
```

**Response:**
```json
{
  "files": [
    {
      "name": "document.pdf",
      "size": 2048576,
      "uploaded_at": "2025-12-12T10:30:00",
      "type": "application/pdf"
    },
    {
      "name": "image.png",
      "size": 512000,
      "uploaded_at": "2025-12-12T10:31:00",
      "type": "image/png"
    }
  ]
}
```

### Download File

**GET** `/api/download/{filename}`

Download a specific file.

```bash
curl "http://localhost:8000/api/download/document.pdf" --output document.pdf
```

### Delete File

**DELETE** `/api/files/{filename}`

Delete a specific file from storage.

```bash
curl -X DELETE "http://localhost:8000/api/files/document.pdf"
```

**Response:**
```json
{
  "message": "File deleted successfully",
  "filename": "document.pdf"
}
```

## 📂 Project Structure

```
fastapi-storage/
│
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
│
└── frontend/              # React + Vite application
    ├── index.html         # HTML entry point
    ├── package.json       # Node.js dependencies
    ├── vite.config.ts     # Vite configuration
    ├── tsconfig.json      # TypeScript configuration
    │
    ├── public/            # Static assets
    │
    └── src/               # React source code
        ├── App.tsx        # Main App component
        ├── main.tsx       # React entry point
        ├── App.css        # App styling
        ├── index.css      # Global styles
        │
        └── assets/        # Images and icons
```

## 🔗 Frontend-Backend Communication

### Architecture

```
┌─────────────────────────────┐
│   React Frontend (Vite)     │
│   - File Upload UI          │
│   - File List Display       │
│   - Download Manager        │
└────────────┬────────────────┘
             │
             │ HTTP/REST API
             │ (JSON)
             │
┌────────────▼─────────────────┐
│   FastAPI Backend            │
│   - Upload Handler           │
│   - File Storage Manager     │
│   - API Endpoints            │
└──────────────────────────────┘
             │
             │ File I/O
             │
┌────────────▼──────────────────┐
│   Local Storage               │
│   - Uploaded Files            │
│   - File Metadata             │
└───────────────────────────────┘
```

### Request Flow

1. **User uploads a file** via the React UI
2. **Frontend sends** a multipart form request to `POST /api/upload`
3. **Backend processes** the file and stores it locally
4. **Backend responds** with success/error status
5. **Frontend updates** the file list by calling `GET /api/files`
6. **User sees** the newly uploaded file in the UI

### Data Exchange Example

**Upload Request:**
```
POST /api/upload HTTP/1.1
Content-Type: multipart/form-data

[Binary file data]
```

**Response:**
```json
{
  "message": "Files uploaded successfully",
  "files": ["example.txt"]
}
```

## 🔮 Future Improvements

- [ ] **User Authentication**: Add login/signup functionality
- [ ] **File Sharing**: Generate shareable links for files
- [ ] **Folder Organization**: Create and manage folders
- [ ] **Search Functionality**: Search files by name or metadata
- [ ] **File Preview**: In-browser preview for images and PDFs
- [ ] **Drag-and-Drop Sorting**: Reorganize files in the UI
- [ ] **File Compression**: ZIP download multiple files
- [ ] **Storage Quotas**: Limit storage per user
- [ ] **Activity Logs**: Track file operations
- [ ] **Dark Mode**: Optional dark theme for UI
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **S3 Integration**: Optional cloud storage backend
- [ ] **File Versioning**: Keep multiple versions of files
- [ ] **API Rate Limiting**: Prevent abuse
- [ ] **WebDAV Support**: Access files via WebDAV protocol

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for the open-source community**

For issues, questions, or contributions, please open an issue or submit a pull request on GitHub.
