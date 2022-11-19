FROM python:3.10
WORKDIR /app
ADD . /app
COPY requirements.txt /app
RUN  pip install -r requirements.txt
EXPOSE 8080
CMD ["python","app.py"]
