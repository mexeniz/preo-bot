## Welcome to Preo Bot Pages

![Preo Bot Logo](/img/preo-bot.png)

Preo Bot is a chat bot for keeping orders on LINE platform. In a chat room, the bot will be your assistant when you and your friends need to collect meal orders.

Version 1.0.1

Logo by [zentinel](https://www.behance.net/zentinel)

### Development

Language: Python3

##### Prerequisite

- line-bot-sdk
- flask
- pytest
- gunicorn

```
pip install line-bot-sdk flask pytest gunicorn
```

#### Test

We use pytest as a test runner.
The name of test functions in 'tests' directory must begin with 'test' or else pytest cannot run those test cases.

```
cd tests
pytest
```

Test with output on console and verbose.

```
pytest -sv
```


#### Run Server

```
export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
python main.py
```

#### Deployment

This project can deploy on Heroku platform.
Heroku platform needs requirements.txt to build an app environment and Procfile to run python app.

### Commands

A chat room can have only one existing order list at the same time.

- Create a new order with name if any. One chat room can have only one opened order at the same time.

```
!new <order_name>
```

- Set new item to the order list

```
!set <user_name> <item> <amount>
```

**Remark** : This command will replace the existing item order.
For example, Preo bot receives a sequence of command like this:

```
!set Jack Milk 3
!set Bob Milk 4
!set Jack Milk 5
!set Bob Milk 2
!set Jack Milk 1
```
Finally, the saved order for Jake will be 1 Milk and the saved order for Bob will be 2 Milk.

- Remove an item from the order list

```
!del <user_name> <item>
```

- Close the current order list. User cannot update the order list but still can list orders.

```
!close
```

- Reopen the closed order list. Then, User can update the order.

```
!open
```

- Show all items in the order list. Each order is grouped by an item name and appended with its amount and a list of ordering users.

```
!list
```

Example list response

```
===== 7-11 Order Summary =====
milk 4: Bob Jack(2) Mike
cocoa 2: Zack Kate
tea 3: Alice(3)
```

- End the current order list. Like list command, a summary of orders will be shown and orders will be cleared.

```
!end
```

- Show help message


```
!help
```

### Support or Contact

Please create an issue if you find bugs or have a comment.
