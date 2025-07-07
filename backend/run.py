from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import file
from rag.handler.singal_handler import SignalHandler

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

app.include_router(file.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# TODO: Import and include routers for file upload and rag functionality 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.run:app", host="0.0.0.0", port=4000, reload=True)