FROM python:3.9-alpine
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
ENV ANIMAL_COUNT=600
ENV FLAG=surctf_i_dr34m_ab0ut_w3bs0cket5_h3lp_m3
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5555", "--ws", "websockets", "--ws-ping-interval", "1000.0", "--ws-ping-timeout", "1000.0"]
