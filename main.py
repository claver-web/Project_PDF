import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form, Request,HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

from Services.ImageResizing import image_resize
from Services.PDFSpliting import Pdf_Reader

app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = [
    "http://127.0.0.1:8000",                # Local dev
    "https://fornt-end-pdf.vercel.app",
    "https://project-pdf-8ve3.onrender.com"    # Render frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],            # ["GET", "POST", "PUT"] for specific methods
    allow_headers=["*"],            # Allow all headers
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "PdfFileStorage")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "OutputPdfFiles")

# Mount the /static path to serve files from the static/ folder
app.mount("/static", StaticFiles(directory="static"), name="static")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/Image_editor/")
async def read_root(request: Request):
    return templates.TemplateResponse("Image_Editor.html", {"request": request})

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

@app.options("/edit_image/")
async def cors_preflight():
    return JSONResponse(content={"status": "ok"})


@app.post("/MultipleUploadfiles/")
async def create_upload_file(
    fromPageNumber: int = Form(...), 
    toPageNumber: int = Form(...),
    file: UploadFile = File(...) ):
    
    # Step 1: Save uploaded file
    # saved_path = os.path.join(OUTPUT_FOLDER, file.filename)
    
    #Step 2: send Info for get Pages
    isFill = Pdf_Reader(file.file, [fromPageNumber, toPageNumber], f"OutputPdfFiles/{os.path.splitext(file.filename)[0]}_{fromPageNumber}.pdf")

    #Step 3: Return processed file if successful
    if isFill is True:
        
        return FileResponse(
            path=f"OutputPdfFiles/{os.path.splitext(file.filename)[0]}_{fromPageNumber}.pdf",
            media_type="application/pdf",
            filename=f"OutputPdfFiles/{os.path.splitext(file.filename)[0]}_{fromPageNumber}.pdf"
        )
    return {"status": "failed"}


@app.post("/edit_image/")
async def edit_image_proccess(
    imag_file: UploadFile = File(...),
    height: int = Form(...),
    width: int = Form(...)
):
    # Save uploaded file
    save_path = os.path.join(BASE_DIR, "img_save", imag_file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(imag_file.file, buffer)

    # Resize and get path to resized image
    resized_path = image_resize(save_path, height, width)

    # Send resized file back
    return FileResponse(
        path=resized_path,
        media_type="image/jpeg",
        filename=os.path.basename(resized_path)  # Optional download filename
    )

@app.get('/remove_files/')
def remove_files():
    folder_path = ["img_save", "OutputPdfFiles"]
    extensions = (".jpg", ".jpeg", ".png", ".pdf")

    for filename in os.listdir(folder_path):

       if filename.lower().endswith(extensions):
            os.remove(os.path.join(folder_path, filename))
