from fastapi import FastAPI, File, Form, UploadFile,Request,status
from transformers import T5Tokenizer, T5ForConditionalGeneration
from io import StringIO
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import logging
import tarfile
import json
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
  return {"Hello":"World"}

@app.get("/basic", response_class=HTMLResponse,name='homepage')
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/training", response_class=HTMLResponse,name = "training")
async def read_item(request: Request):
    num = 100
    return templates.TemplateResponse("next.html", {"request": request, "num": num})

# @app.post("/basic")
# async def get_form(request: Request,sample: str = Form(...), label: str = Form(...),templates: str = Form(...),one: str = Form(...), two: str = Form(...),model_para: str = Form(...),file: UploadFile = File(...)):
#     file_upload = tarfile.open(fileobj=file.file, mode="r:gz")
#     file_upload.extractall('./data_uploaded')
#     print(f'sample:{sample}')
#     print(f'label:{label}')
#     print(f'sample:{templates}')
#     print(f'1:{one}')
#     print(f'2:{two}')
#     print(f'model_para:{model_para}')
#     para_dic = {"sample":sample,"label":label,"templates":templates,"one":one,"two":two,"model_para":model_para}
#     with open('data.json', 'w') as f:
#         json.dump(para_dic, f)
#     redirect_url = request.url_for('racia')
#     return RedirectResponse(redirect_url, status_code=303)
@app.post("/basic")
async def get_form(request: Request,file: UploadFile = File(...)):
    file_upload = tarfile.open(fileobj=file.file, mode="r:gz")
    file_upload.extractall('./data_uploaded')
    da = await request.form()
    da = jsonable_encoder(da)
    templates_counter = 1
    origin_counter = 1
    mapping_counter = 1
    para_dic = {"sample": da["sample"], "label": da["label"], "templates": da["templates"], "origin": da["origin"], "mapping": da["mapping"],
                "model_para": da["model_para"]}
    while f"templates_{str(templates_counter)}" in da:
        template_key = f"templates_{str(templates_counter)}"
        para_dic[template_key] = da[template_key]
        templates_counter = templates_counter+1
    while f"origin_{str(origin_counter)}" in da:
        origin_key = f"origin_{str(origin_counter)}"
        para_dic[origin_key] = da[origin_key]
        origin_counter = origin_counter+1
    while f"mapping_{str(mapping_counter)}" in da:
        mapping_key = f"mapping_{str(mapping_counter)}"
        para_dic[mapping_key] = da[mapping_key]
        mapping_counter = mapping_counter+1
    with open('data.json', 'w') as f:
        json.dump(para_dic, f)
    redirect_url = request.url_for('training')
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

