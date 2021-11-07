FROM tiangolo/uvicorn-gunicorn-fastapi

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","80"]