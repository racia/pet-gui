from fastapi import FastAPI, File, UploadFile,Request,status
from transformers import T5Tokenizer, T5ForConditionalGeneration
from io import StringIO
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import logging
import tarfile
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
  return {"Hello":"World"}

@app.get("/basic", response_class=HTMLResponse,name='homepage')
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/basic")
async def get_form(request: Request,file: UploadFile = File(...)):
    file_upload = tarfile.open(fileobj=file.file, mode="r:gz")
    file_upload.extractall('./data_uploaded')
    redirect_url = request.url_for('homepage')
    return RedirectResponse(redirect_url, status_code=303)




    #return redirect(url_for('delete_images'))
    # redirect_url = request.url_for('basic_upload')
    # return RedirectResponse(redirect_url, status_code=303)

    # return {"filename": file.filename,"info":"upload successful"}

    #return templates.TemplateResponse("basic_upload.html", {"request": request})


# <input type='file' .... onchange='this.form.submit();'><br><br>

#
#
#
#
#
#
# from transformers import T5Tokenizer, T5ForConditionalGeneration
# @app.post("/translate_the_text")
# def translate_text(file: UploadFile = File(...)):
#     contents = file.file.read()
#     with open(file.filename,'wb') as f:
#         f.write(contents)
#     with open(file.filename) as file:
#         tras_data = file.read()
#     tokenizer = T5Tokenizer.from_pretrained('t5-small')
#     model = T5ForConditionalGeneration.from_pretrained('t5-small', return_dict=True)
#     input_ids = tokenizer("translate English to German: "+tras_data, return_tensors="pt").input_ids  # Batch size 1
#     outputs = model.generate(input_ids)
#     decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     with open("translated_text.txt","w") as q:
#         q.write(decoded)
#     file_location = "translated_text.txt"
#     return FileResponse(file_location, media_type='text/txt', filename="translated_text.txt")
   # # return {
   #          "input_text": tras_data,
   #          "translation_text": decoded
   #         }

# @app.get("/download-file")
# def download_file(upload_file):
#     file_path = upload_file.filename
#     return FileResponse(path=file_path, filename=file_path)

