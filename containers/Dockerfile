FROM python:3.6-slim
COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./trained_model.pkl /deploy/
WORKDIR /deploy/
RUN pip install -r requirements.txt
EXPOSE 8088
ENTRYPOINT ["python", "app.py"]