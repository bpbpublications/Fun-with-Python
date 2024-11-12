from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main():
    url = "http://foo.com/redirect"
    return {"url": url}
