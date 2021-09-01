FROM python:3.7
COPY requirements.txt ./
COPY companiesRegistry.py ./
RUN pip install -r ./requirements.txt
EXPOSE 8000
CMD exec uvicorn --log-level info --timeout-keep-alive 0 --host 0.0.0.0 --port 8000 companiesRegistry:app