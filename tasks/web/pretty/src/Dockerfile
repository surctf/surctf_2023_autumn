FROM python:3.11-alpine

WORKDIR pretty

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup -S surctf && adduser -S surctf_secret_is_not_s3cret_if_u_kn0w_t1mestamp -G surctf
USER surctf_secret_is_not_s3cret_if_u_kn0w_t1mestamp

ENTRYPOINT python main.py
#ENTRYPOINT bash