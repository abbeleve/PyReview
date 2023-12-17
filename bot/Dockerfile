FROM python:3.9

COPY . /bot/

WORKDIR /bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --force-reinstall -v "aiogram==2.23.1"

CMD python bot.py