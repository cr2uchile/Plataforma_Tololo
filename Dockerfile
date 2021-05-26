FROM python:3.8.0-buster

WORKDIR /App

COPY . .

COPY requirements.txt .
COPY * ./
RUN pip install -r requirements.txt

#COPY . App/ 

EXPOSE 8050

CMD ["python","/App/Tololo_Interfaz_Final.py"]

