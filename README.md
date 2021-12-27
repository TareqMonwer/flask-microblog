### Setup:
After setting up the virtual-environment, run these commands in your terminal:
+ `pip install -r requirements.txt`
+ `export FLASK_APP=microblog.py`
+ `flask run`

#### Fake Development Mail Server Config:
+ do `export MAIL_SERVER=localhost`
+ `export MAIL_PORT=8025`
+ `export FLASK_DEBUG=0`
+ then start console by running this command: <br> `python -m smtpd -n -c DebuggingServer localhost:8025`
