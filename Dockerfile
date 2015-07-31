FROM python:2.7.10
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV MODE DEVELOPMENT
#CMD nohup "gunicorn -w 2 App:app -b 0.0.0.0:80 &"
#CMD ["nohup", "gunicorn -w 2 App:app -b 0.0.0.0:80 &"]
#CMD ["gunicorn","-w 2","run:app","-b 0.0.0.0:80"]
CMD ["python","run.py"]