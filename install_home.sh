#!/bin/sh

cp ./radio_listner/radio_listner.py /opt/.
cp ./radio_listner/radio_listner.service /etc/systemd/system/.
systemctl enable radio_listner
systemctl stop radio_listner
systemctl start radio_listner

cp ./rpi_reporter/rpi_reporter.py /opt/.
cp ./rpi_reporter/rpi_reporter.service /etc/systemd/system/.
systemctl enable rpi_reporter
systemctl stop rpi_reporter
systemctl start rpi_reporter

