### ClockTower

<img src="./clocktower.png" style="zoom: 67%;" />

A telegram bot made with python

#### Features:

1. Welcome Message while entering the group
2. Calculator (Validates expression and timeouts if expensive)
3. Echo message
4. Error Handler
5. Feedback
6. Morse Code
7. Text to QR Code
8. Get random quote from [quotable](https://github.com/lukePeavey/quotable)
9. Get shareable link for an image
10. Get query definition from [Urban Dictionary](https://api.urbandictionary.com/v0/define?term=urban%20dictionary)
11. MongoDB for caching API responses

#### Requirements:

- Python 3.8 or above
- [python-telegram-bot](https://python-telegram-bot.org/)
- [Requests](https://docs.python-requests.org/en/master/)
- [pymongo](https://github.com/mongodb/mongo-python-driver)
- [qrcode](https://github.com/lincolnloop/python-qrcode)

#### Installation & Usage
1. Clone Repo
   
   ```bash
   git clone https://github.com/shelldoom/ClockTower.git
   ```
   
1. Install dependencies
	```bash
	pip3 install -r requirements.txt
	```
1. Setup config.ini
1. Setup MongoDB
1. Run `main.py`

#### Todo list:

1. Change to Redis
