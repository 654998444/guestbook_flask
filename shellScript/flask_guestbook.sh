#!/bin/bash

python3 /home/ec2-user/guestbook_flask/flask_guestbook.py &> /var/log/flask_guestbook-$(date +%y-%m-%d).log 
