#!/bin/sh

echo "Check radio_listner.py"
diff ./radio_listner/radio_listner.py /opt/radio_listner.py
echo "Check radio_listner.service"
diff ./radio_listner/radio_listner.service /etc/systemd/system/radio_listner.service

echo "Check rpi_reporter.py"
diff ./rpi_reporter/rpi_reporter.py /opt/rpi_reporter.py
echo "Check rpi_reporter.service"
diff ./rpi_reporter/rpi_reporter.service /etc/systemd/system/rpi_reporter.service

