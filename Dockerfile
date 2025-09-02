# image base and version
FROM python:3.12.11

# enviroment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

# Create directory
WORKDIR /app

#RUN adduser django
#RUN chown django:django /app
#USER django
ENV PATH /home/django/.local/bin:$PATH

# Install requirements
COPY requirements.txt .
COPY prod_requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r prod_requirements.txt

# Copy repository to directory
COPY . ./

RUN mkdir static
RUN mkdir media

RUN apt update
RUN apt install gettext -y

# Setup start commands
# RUN python manage.py migrate
# CMD ["gunicorn","--bind","0.0.0.0:8000","website.wsgi"]
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
