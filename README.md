# joda-kev20

Ohjeet täydentyvät pikku hiljaa. Toivottavasti


Haven't really done that much yet. StreamListener collects tweets and saves them to tweets2.db.

Most of the stuff I've written in notebooks is in MainNotebook.ipynb. Thus far, I've tried to make
a weighted graph network out of hashtags that co-occur in tweets, sort of like this:
https://stackoverflow.com/questions/58803155/creating-a-weighted-network-from-co-occurence-of-hashtags-from-a-dataframe

Database schema:

```
CREATE TABLE tweets (
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	tweet_id TEXT, 
	user_id TEXT, 
	screen_name TEXT, 
	is_retweet BOOLEAN, 
	is_quote BOOLEAN, 
	text TEXT, 
	quoted_text TEXT, 
	lang TEXT, 
	PRIMARY KEY (id), 
	CHECK (is_retweet IN (0, 1)), 
	CHECK (is_quote IN (0, 1))
);
CREATE TABLE hashtags (
	id INTEGER NOT NULL, 
	hashtag TEXT, 
	esiintynyt BIGINT, 
	PRIMARY KEY (id)
);
CREATE TABLE tweet_tags (
	id INTEGER NOT NULL, 
	tweet_id TEXT, 
	tag_id BIGINT, 
	PRIMARY KEY (id)
);
```

# Setting up

We're not here to break things - hopefully!. Therefore, let's set up a virtual environment that doesnt' interfere with your system's python.

First of all, we're using python 3.7 here, so if you have an earlier version, you're going to want to update it. These are very good [instructions](https://copdips.com/2019/10/installing-python3-on-ubuntu.html) for accomplishing that, although you'll have to modify them a bit to suit your needs.
