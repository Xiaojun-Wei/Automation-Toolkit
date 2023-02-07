FROM python:3.7
LABEL maintainer="jessiewei747@gmail.com" 
WORKDIR /app
COPY . .
RUN pip install -r /app/requirements.txt
EXPOSE 5000
CMD ["python app.py"] 
