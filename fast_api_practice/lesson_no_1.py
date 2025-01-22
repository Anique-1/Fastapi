from fastapi import FastAPI  
app = FastAPI()   
@app.get("/") 
async def main_route():     
  return {"message": "Hey, It is me Goku"}

@app.post("/home{message}")
def home(message):
  return {"message": f"Hello, {message}!"}