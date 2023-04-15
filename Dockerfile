FROM python:3-alpine3.16
WORKDIR /app
COPY . /app
RUN pip install -r requirement.txt
EXPOSE 3000
CMD [ "flask.exe --app .\src\api.py run " ]
