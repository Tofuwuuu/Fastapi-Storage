models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="File Storage API", version="1.0.0")

#Cors
app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "Welcome to File Storage API",
        "docs": "Visit http://localhost:8000/docs for API documentation"
    }

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):