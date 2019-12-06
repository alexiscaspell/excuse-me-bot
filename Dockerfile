FROM python:3.7

# --------------------------------------
# AMBIENTE PREDEFINIDO
# --------------------------------------

ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_GUNICORN_WORKERS=2
ENV PYTHON_GUNICORN_CONNECTIONS=500
ENV PYTHON_NOMBRE_APP=app
ENV PYTHON_NOMBRE_FUNCION_APP=app


# --------------------------------------
# EJECUCION
# --------------------------------------

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

WORKDIR /usr/src/
RUN chmod 777 . -R

COPY . .

RUN pip install -r requirements.txt --upgrade pip

EXPOSE ${PORT}

CMD gunicorn \
    -b ${PYTHON_HOST}:${PORT} \
    --reload \
    --workers=${PYTHON_GUNICORN_WORKERS} \
    --worker-connections=${PYTHON_GUNICORN_CONNECTIONS} \
    ${PYTHON_NOMBRE_APP}:${PYTHON_NOMBRE_FUNCION_APP}
