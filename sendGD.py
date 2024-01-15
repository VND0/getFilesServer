from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()


@app.get("/geometry")
def get_file():
    return FileResponse(path="~/geometry-dash-2.11-by-great-crafter.rar", filename="archive.rar",
                        media_type="multipart/form-data")


if __name__ == '__main__':
    uvicorn.run(app)  # Add host and port on server.
