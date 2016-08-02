FROM python:3-onbuild
EXPOSE 8000
CMD gunicorn couchdb_download_token:api -b 0.0.0.0:8000
