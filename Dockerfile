# 
FROM python:3.9

#
WORKDIR /code

# Get all requirements for FastApi and Pet
COPY requirements.txt /code/requirements.txt

#
RUN python -m pip install --upgrade pip

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY /app /code/app

#
COPY /setup.py /code/setup.py

#
#COPY /Pet /code/Pet

#
COPY /templates /code/templates

#
COPY /Dockerfile /code/Dockerfile

#
RUN pip install .

#
RUN chmod -R a+rwx /code

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
