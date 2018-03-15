## Welcome to Preo Bot Pages

Preo Bot is a preorder helper bot for Line platform.

### Development

Language: Python

##### Prerequisite

- line-bot-sdk
- flask

```
pip install line-bot-sdk flask
```

#### Run Server

```
export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
python main.py
```

### Commands

```
1. !preorder <name>
2. !add <user> <order> <total>
3. !del <user> <order> <total>
4. !endorder
5. !list <name|ID>
6. !help
```

### Support or Contact

Please create an issue if you find bugs or have a comment.
