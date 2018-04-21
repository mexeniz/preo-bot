## Welcome to Preo Bot Pages

Preo Bot is a preorder helper bot for Line platform.

Version 0.0.3

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

- Add new item to the order list

```
!add <user_name> <item> <amount>
```

**Remark** : This command will replace the existing item order.
For example, Preo bot receives a sequence of command like this:

```
!add Jack Milk 3
!add Bob Milk 4
!add Jack Milk 5
!add Bob Milk 2
!add Jack Milk 1
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
!reopen
```

- End the current order list. All orders will be cleared.

```
!end
```

- Show all items in the order list

```
!list
```

- Show help message

```
!help
```

### Support or Contact

Please create an issue if you find bugs or have a comment.
