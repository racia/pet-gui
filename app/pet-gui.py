from fastapi import FastAPI, File, Form, UploadFile, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import tarfile
import json
from Pet import script
from Pet.examples import custom_task_pvp, custom_task_processor

app = FastAPI()

try:
    templates = Jinja2Templates(directory="/fastapi/templates")  # cluster
    app.mount("/static", StaticFiles(directory="/fastapi/static"), name="static")
except:
    templates = Jinja2Templates(directory="templates")  # local
    app.mount("/static", StaticFiles(directory="static"), name="static")


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
    Starts training with params and data_uploaded in Pet directory.
    """
    instance = script.Script("pet", [0, 1, 2, 3], "Pet/data_uploaded/yelp_review_polarity_csv/", "bert", "bert-base-cased",
                      "yelp-task", "./output")  # set defined task name
    instance.run()


@app.get("/train", name="train")
async def kickoff(background_tasks: BackgroundTasks):
    """
    Kicks off training by calling train method as background task with defined task name.
    """
    try:
        with open("data.json", "r") as f:  # local
            data = json.load(f)
    except:
        with open("/fastapi/data.json", "r") as f:  # cluster
            data = json.load(f)

    '''Configure Data Preprocessor'''
    # define task name
    custom_task_processor.MyTaskDataProcessor.TASK_NAME = "yelp-task"
    # define labels
    custom_task_processor.MyTaskDataProcessor.LABELS = ["1", "2"]
    # define samples column
    custom_task_processor.MyTaskDataProcessor.TEXT_A_COLUMN = int(data["sample"])
    # define labels column
    custom_task_processor.MyTaskDataProcessor.LABEL_COLUMN = int(data["label"])
    # save entries as new task
    custom_task_processor.report() # save task

    '''Configure Verbalizers'''
    custom_task_pvp.MyTaskPVP.TASK_NAME = "yelp-task"
    # define verbalizer for label 1
    custom_task_pvp.MyTaskPVP.VERBALIZER["1"].append(data["one"])
    # define verbalizer for label 2
    custom_task_pvp.MyTaskPVP.VERBALIZER["2"].append(data["two"])
    # save entries as new task
    custom_task_pvp.report() # save task

    '''Start Training'''
    background_tasks.add_task(train)
    return {"Training started with params:": data}


@app.post("/basic")
async def get_form(request: Request,sample: str = Form(...), label: str = Form(...),templates: str = Form(...),one: str = Form(...), two: str = Form(...),model_para: str = Form(...),file: UploadFile = File(...)):
    file_upload = tarfile.open(fileobj=file.file, mode="r:gz")
    file_upload.extractall('./Pet/data_uploaded') # upload directly into Pet folder
    print(f'sample:{sample}')
    print(f'label:{label}')
    print(f'templates:{templates}')
    print(f'1:{one}')
    print(f'2:{two}')
    print(f'model_para:{model_para}')
    para_dic = {"sample":sample,"label":label,"templates":templates,"one":one,"two":two,"model_para":model_para}
    with open('data.json', 'w') as f:
        json.dump(para_dic, f)
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

