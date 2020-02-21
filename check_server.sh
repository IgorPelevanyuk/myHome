#!/bin/sh

diff ./server/zmq_receiver.service /etc/systemd/system/zmq_receiver.service 
diff ./server/rest_server.service /etc/systemd/system/rest_server.service
diff ./server/telegram_reporter.service /etc/systemd/system/telegram_reporter.service

diff ./server/Server.py /opt/server/Server.py
diff ./server/TelegramBot.py /opt/server/TelegramBot.py
diff ./server/Receiver.py /opt/server/Receiver.py


