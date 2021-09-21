FROM python:3.6

WORKDIR /celery_worker

#Install celery
RUN pip install celery
RUN pip install redis

#Install exquiro
RUN pip install lxml
RUN pip install neomodel
RUN pip install -i https://test.pypi.org/simple/ exquiro==0.3.3
# Install package
COPY . .