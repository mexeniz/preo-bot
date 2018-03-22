## Welcome to Preo Bot Pages

Preo Bot is a preorder helper bot for Line platform.

### Development

Language: Python

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

#### Run Server

```
export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
python main.py
```

#### Deployment

This project can deploy on Heroku platform.

### Commands

- A chat room can have only one existing order list at the same time.

```
1. !new
2. !add <order> <total>
3. !del <order> <total>
4. !end
5. !list
6. !help
```

### Support or Contact

Please create an issue if you find bugs or have a comment.
