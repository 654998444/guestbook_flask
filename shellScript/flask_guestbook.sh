#!/bin/bash

python3 /home/ec2-user/guestbook_flask/flask_guestbook.py &> ~/flask_guestbook-$(date +%Y-%m-%d).log 
