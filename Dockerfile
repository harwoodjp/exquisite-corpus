FROM python:3.8
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD . /code
WORKDIR /code
EXPOSE 1993
CMD ["export", "FLASK_APP=app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=1993"]

