from fastapi import FastAPI, Request, HTTPException
import os
import time 

app = FastAPI()
SAVE_DIR = os.environ.get("SAVE_DIR", "recordings")
os.makedirs(SAVE_DIR, exist_ok=True)



@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/upload")
async def upload(request: Request):
    sent_key = request.headers.get("x-device-key")
    expected_key = os.environ.get("DEVICE_KEY")
    if not expected_key or sent_key != expected_key:
        raise HTTPException (status_code=401)
    audio = await request.body()
    if not audio:
        raise HTTPException(status_code=400, detail="empty body")
    # return {"bytes": len(audio)}
    filename = f"rec_{int(time.time())}.wav"
    path = os.path.join(SAVE_DIR,filename)
    with open(path,"wb") as f:
        f.write(audio)
    return {"saved":filename,"bytes":len(audio)}

