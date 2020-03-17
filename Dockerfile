FROM python:3

ADD bot.py /
ADD token.secret /
ADD help.txt /

RUN pip install discord.py
RUN pip install requests

CMD [ "python", "./bot.py" ]
