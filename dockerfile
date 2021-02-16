FROM python:3.9.1-slim-buster

ADD requirements.txt /
ADD tokens.py /
ADD sakugabot_tg.py /
ADD sakugabot_vk.py /
ADD post_id.txt /
ADD tag.json /
ADD vk_config.v2.json /

RUN pip install -r requirements.txt

CMD ["python3", "./sakugabot_tg.py"]