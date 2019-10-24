FROM alpine:latest

MAINTAINER shimona prabhu <shimprab@cisco.com>

RUN apk add --no-cache python3-dev \
    && apk add --no-cache py-pip \
    && pip install --upgrade pip \
    && apk add python python-dev py-pip build-base libffi-dev openssl-dev libgcc 
    

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]