FROM NINJAHACKER01/NinjaBOT:slim-buster

#clonning repo 
RUN git clone https://github.com/NINJABOT2/NINJABOT2.0.git /root/userbot
#working directory 
WORKDIR /root/userbot

# Install requirements
RUN pip3 install --no-cache-dir requirements.txt

ENV PATH="/home/userbot/bin:$PATH"

CMD ["python3","-m","userbot"]
