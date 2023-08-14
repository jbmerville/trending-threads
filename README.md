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
aws scheduler create-schedule --schedule-expression "at(2023-08-10T17:10:00)" --name schedule-name \
--target '{"RoleArn": "role-arn", "Arn": "QUEUE_ARN", "Input": "TEST_PAYLOAD" }' \
--schedule-expression-timezone "Europe/Paris"
--flexible-time-window '{ "Mode": "OFF"}'

aws scheduler create-schedule --schedule-expression "at(2023-08-10T17:10:00)" --name schedule-name \
--target '{"RoleArn": "role-arn", "Arn": "arn:aws:sqs:eu-west-1:782309524155:TrendingThread-Queue", "Input": {
  "thread_name": "Luke Bryan",
  "thread_content": [
  "Luke Bryan just wrapped up American Idol & is looking forward to spending quality time with his family. He's ready to whisk his wife off to somewhere tropical after a hectic year. #LukeBryan #AmericanIdol #FamilyTime ",
  "Luke Bryan is suspected to return to his role as a judge on American Idol, while also releasing new music & returning to his Las Vegas residency. #LukeBryan #AmericanIdol #Music ",
  "Luke Bryan recently shared an unreleased new song on Instagram, listen to it below. #LukeBryan #AmericanIdol #Music"
],
  "account_name": "trends_account",
  "image_url": "https://news3lv.com/resources/media2/16x9/full/1015/center/80/ded1fcce-0378-4ef5-83cd-6400001c7520-large16x9_LukeBryanVegas2.11.22CreditJohnShearer3.jpg",
} }' \
--schedule-expression-timezone "Europe/Paris"
--flexible-time-window '{ "Mode": "OFF"}'
```

Schedule a thread to be posted to twitter at an interval:

```
TODO
```
