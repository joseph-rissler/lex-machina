FROM python:3.11-alpine
WORKDIR /Application
ADD src ./
RUN pip install discord
ENTRYPOINT ["python", "main.py"]

