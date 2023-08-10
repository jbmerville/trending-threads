# Trending Threads

Trending Threads is a Python script that generates twitter threads on the latest trends.

It also has an AWS infrastructure to schedule posting threads at a specify date or at intervals. It also allows to post from different accounts.

### Setup

Copy the `config/settings_template.py` to `config/settings.py` and enter your api keys.

### Script

TODO

### Schedule Posts

First you need to setup the AWS infrastructure with:

```
cdk bootstrap
cdk deploy
```

Add secrets to AWS secret manager with:

```
aws secretsmanager put-secret-value --secret-id "twitter/credentials/${account_name}" --secret-string '{"api_key":"value","api_secret":"value","access_token":"value","access_token_secret":"value"}'
```

Schedule a thread to be posted to twitter for a specify date:

```
TODO
```

Schedule a thread to be posted to twitter at an interval:

```
TODO
```
