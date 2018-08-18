#!/bin/sh

diff ./radio_listner/radio_listner.py /opt/radio_listner.py
diff ./radio_listner/radio_listner.service /etc/systemd/system/radio_listner.service

