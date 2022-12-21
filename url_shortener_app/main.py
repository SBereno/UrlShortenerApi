import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import model, schema, session, config, keygen
import validators
import uvicorn
from starlette.datastructures import URL

app = FastAPI()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@app.get("/")
def read_root():
    return {"message": "Server is up and running!"}


@app.get("/{url_key}")
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(session.create_get_session)):
    if db_url := keygen.get_db_url_by_key(db=db, url_key=url_key):
        db_url.clicks += 1
        db.commit()
        db.refresh(db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


@app.post('/url', response_model=schema.url_schema, status_code=201)
async def create_url(url: schema.url_schema, db: Session = Depends(session.create_get_session)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    base_url = URL(config.get_settings().base_url)
    key = keygen.create_unique_random_key(db)
    shorted_url = str(base_url.replace(path=key))
    new_url = model.Url(
        key=key,
        target_url=url.target_url
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    new_url.key = shorted_url
    return new_url

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")