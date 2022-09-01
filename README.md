# kuro-store-django

Web App to create stores, sell and buy (not real purchases)

### Docker Image

You can run this project with the [docker image](https://hub.docker.com/r/kurovale/kuro-store) of this project

## Prerequisites
**Making venv**

Make a virtual environment by running:

```py -m venv venv```

To activate run:

In windows: 
```.\venv\Scripts\activate```

In Linux: 
```source venv/bin/activate```

**Installing dependencies**

Install all dependencies that are required for the project by running:

```pip install -r requirements.txt```

## Running django server

```bash
cd kuro-store-django
```
```bash
python3 manage.py runserver
```

Visit 127.0.0.1:8000/ to see the web app