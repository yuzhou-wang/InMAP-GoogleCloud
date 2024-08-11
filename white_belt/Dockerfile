FROM python:3.8.0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app.py  app.py
COPY WhiteBeltService.py  WhiteBeltService.py
COPY LlmInmap.py  LlmInmap.py
COPY LlmQuery.py  LlmQuery.py
COPY latlon_cross.csv  latlon_cross.csv

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
