FROM python:3.10

# Create the directory for the container
WORKDIR /fastapi

# Get all requirements for FastApi and Pet
COPY requirements.txt /fastapi/requirements.txt

#
COPY /app /fastapi/app

#
COPY /static /fastapi/static

#
COPY /Pet /fastapi/Pet

#
COPY /setup.py /fastapi/setup.py

#
COPY /templates /fastapi/templates

#
COPY /Dockerfile /fastapi/Dockerfile

#
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /fastapi/requirements.txt && \
    pip install .

# Run by specifying the host and port
CMD ["uvicorn", "app.pet-gui:app", "--host", "0.0.0.0", "--port", "8080"]
