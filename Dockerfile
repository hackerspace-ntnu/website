FROM python:3.6.0
RUN apt-get update
RUN pip install --upgrade pip
RUN mkdir /code
RUN mkdir /gunicorn-logfiles
COPY requirements.txt /code/
COPY prod_requirements.txt /code/
RUN pip install -r /code/requirements.txt
RUN pip install -r /code/prod_requirements.txt
WORKDIR /code
CMD ["bash", "/code/entrypoint.sh"]
