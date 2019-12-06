 
FROM python:3.7

RUN pip install python-telegram-bot

WORKDIR /usr/src/
RUN chmod 777 . -R

COPY . .

RUN pip install -r requirements.txt --upgrade pip

CMD python bot.py