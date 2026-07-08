from fastapi import FastAPI

app = FastAPI(
    title="Smart AI CNG Station Management System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Smart AI CNG Station Management System API is running"
    }