Первый коммерческий проект, связан с backend разработкой на python, FastApi.


1) python -m venv venv
2) pip install -r requirements.txt
3) uvicorn app.main:app --reload

1) sudo systemctl list-unit-files
2) sudo systemctl status gunicorn.service
3) sudo systemctl start gunicorn.service
4) sudo systemctl status gunicorn.service
5) sudo systemctl enable gunicorn.service 
