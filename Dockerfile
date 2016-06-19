FROM python:3.5.1
RUN apt-get update
RUN mkdir /code
RUN mkdir /gunicorn-logfiles
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
WORKDIR /code
CMD ["sh", "/code/entrypoint.sh"]
