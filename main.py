import os
import aiofiles
from fastapi import FastAPI, File, UploadFile, Form, Request,HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from Services.PDFSpliting import Pdf_Reader
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "PdfFileStorage")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "OutputPdfFiles")

# Mount the /static path to serve files from the static/ folder
app.mount("/static", StaticFiles(directory="static"), name="static")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/uploadfile/")
async def create_upload_file(pages: int = Form(...), file: UploadFile = File(...)):
    
    # Step 1: Save uploaded file
    saved_path = os.path.join(OUTPUT_FOLDER, file.filename)
    
    # Step 2: send Info for get Pages
    isFill = Pdf_Reader(file.file, [pages], f"OutputPdfFiles/{os.path.splitext(file.filename)[0]}_{pages}.pdf")

    # Step 3: Return processed file if successful
    if isFill is True:
        
        return FileResponse(
            path=f"OutputPdfFiles/{os.path.splitext(file.filename)[0]}_{pages}.pdf",
            media_type="application/pdf",
            filename=f"OutputPdfFiles/{os.path.splitext(file.filename)[0]}_{pages}.pdf"
        )

    return {"status": "failed"}


@app.post("/MultipleUploadfiles/")
async def create_upload_file(
    fromPageNumber: int = Form(...), 
    toPageNumber: int = Form(...),
    file: UploadFile = File(...) ):
    
    # Step 1: Save uploaded file
    # saved_path = os.path.join(OUTPUT_FOLDER, file.filename)
    
    # # Step 2: send Info for get Pages
    isFill = Pdf_Reader(file.file, [fromPageNumber, toPageNumber], f"OutputPdfFiles/{os.path.splitext(file.filename)[0]}_{fromPageNumber}.pdf")

    # # Step 3: Return processed file if successful
    if isFill is True:
        
        return FileResponse(
            path=f"OutputPdfFiles/{os.path.splitext(file.filename)[0]}_{fromPageNumber}.pdf",
            media_type="application/pdf",
            filename=f"OutputPdfFiles/{os.path.splitext(file.filename)[0]}_{fromPageNumber}.pdf"
        )
    return {"status": "failed"}

    # return {"status": "failed"}