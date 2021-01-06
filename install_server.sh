#!/bin/sh

cp -r ./server /opt/.
chmod +x /opt/server/Server.py
chmod +x /opt/server/TelegramBot.py
chmod +x /opt/server/Receiver.py


cp ./server/zmq_receiver.service /etc/systemd/system/.
systemctl enable zmq_receiver
systemctl stop zmq_receiver
systemctl start zmq_receiver

cp ./server/rest_server.service /etc/systemd/system/.
systemctl enable rest_server
systemctl stop rest_server
systemctl start rest_server

cp ./server/telegram_reporter.service /etc/systemd/system/.
systemctl enable telegram_reporter
systemctl stop telegram_reporter
systemctl start telegram_reporter

systemctl status zmq_receiver
systemctl status rest_server
systemctl status telegram_reporter

