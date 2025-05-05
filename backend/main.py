from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, report

app = FastAPI()

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(upload.router, prefix="/upload")
app.include_router(report.router, prefix="/report")

@app.get("/")
def read_root():
    return {"status": "backend running"}
