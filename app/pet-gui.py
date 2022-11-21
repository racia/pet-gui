from fastapi import FastAPI, File, UploadFile, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import tarfile
from Pet import script

app = FastAPI()

templates = Jinja2Templates(directory="/fastapi/templates")

app.mount("/static", StaticFiles(directory="/fastapi/static"), name="static")


@app.get("/")
async def read_root():
  return {"Hello": "World"}


@app.get("/basic", response_class=HTMLResponse, name='homepage')
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/progress", response_class=HTMLResponse, name="progress")
async def read_item(request: Request):
    num = 100
    return templates.TemplateResponse("progress.html", {"request": request, "num": num})


def train():
    """
    Starts training with (yet) hardcoded params and data_uploaded in Pet directory.
    """
    instance = script.Script("pet", [0, 1, 2, 3], "Pet/data_uploaded/yelp_review_polarity_csv/", "bert", "bert-base-cased",
                      "yelp-polarity", "./output")
    instance.run()

@app.get("/train", name="train")
async def kickoff(background_tasks: BackgroundTasks):
    """
    Kicks off training by calling train method as background task.
    """
    background_tasks.add_task(train)
    return {"message": "Training started"}


@app.post("/basic")
async def get_form(request: Request, file: UploadFile = File(...)):
    file_upload = tarfile.open(fileobj=file.file, mode="r:gz")
    file_upload.extractall('./Pet/data_uploaded') # upload directly into Pet folder
    redirect_url = request.url_for('train')
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

