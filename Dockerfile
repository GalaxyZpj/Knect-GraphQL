FROM python:alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "python3" ]
