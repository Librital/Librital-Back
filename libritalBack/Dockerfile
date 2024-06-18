FROM python:3.12.1

RUN mkdir /app
ADD . /app
WORKDIR /app

EXPOSE 8000

RUN pip install -r /app/requirements.txt
RUN ls
CMD ["python",  "manage.py",  "runserver",  "0.0.0.0:8000"]