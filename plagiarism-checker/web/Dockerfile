FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install ./en_trf_bertbaseuncased_lg-2.2.0.tar.gz

CMD [ "python", "app.py" ]