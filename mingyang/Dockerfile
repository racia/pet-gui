FROM python:3.9

# Create the directory for the container
WORKDIR /fastapi

# Install the dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install transformers
#RUN pip install uvicorn
#RUN pip install fastapi
#RUN pip install sentencepiece
#RUN pip3 install torch torchvision torchaudio
COPY pet-gui.py /fastapi/pet-gui.py
COPY static /fastapi/static
COPY templates /fastapi/templates
COPY requirements.txt /fastapi/requirements.txt
COPY setup.py /fastapi/setup.py
RUN pip install --no-cache-dir --upgrade -r /fastapi/requirements.txt
RUN pip install .



# Copy the serialized model and the vectors
#COPY ./models/spam_detector_model.pkl ./models/spam_detector_model.pkl
#COPY ./vectors/vectorizer.pickle ./vectors/vectorizer.pickle

# Run by specifying the host and port
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
