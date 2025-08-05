from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from PDFSpliting import Pdf_Reader

# for saving the file that came from the client
import aiofiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#Using post method for saving the files that came from client
@app.post("/uploadfile/")
async def create_upload_file(pages: int = Form(...), file: UploadFile = File(...)):
    print(pages, file.filename)
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # if file.size > 1024 * 1024:  # 1MB
    #     raise HTTPException(status_code=400, detail="File too large")
    
    async with aiofiles.open(file.filename, mode="wb") as f:
        await f.write(await file.read())
        
        isFill = Pdf_Reader(file.filename, [1], 'output.pdf')
        
        if isFill == True:
            #If file is large than use this 
            async def file_stream():
                async with aiofiles.open(file_path, mode="rb") as file:
                    while chunk := await file.read(1024 * 1024):
                        yield chunk
                        
            return FileResponse('output.pdf', media_type="application/pdf")
        
        return {"filename": isFill}
