FROM --platform=$BUILDPLATFORM python:3.10-slim
# AS builder
EXPOSE 8000
WORKDIR /app
COPY requirements.txt .
COPY prod_requirements.txt .
RUN pip3 install -r prod_requirements.txt --no-cache-dir
COPY . .

ENTRYPOINT ["/bin/bash"]
CMD ["./startup.sh"]

# FROM builder as dev-envs
# RUN <<EOF
# apk update
# apk add git
# EOF

# RUN <<EOF
# addgroup -S docker
# adduser -S --shell /bin/bash --ingroup docker vscode
# EOF
# # install Docker tools (cli, buildx, compose)
# COPY --from=gloursdocker/docker / /
# CMD ["manage.py", "runserver", "0.0.0.0:8000"]
