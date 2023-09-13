# Access Token: 1389604087696609283-BanTACWIXqfglKtF8OacGA3u7qwxf1
# Access Token Secret: e9HxWCOnINg8ghgl9mfkccT3TsTFcZPr3NzcPmXsL9zri
# Bearer Token: AAAAAAAAAAAAAAAAAAAAAPEOpwEAAAAAVHvsNit2Av0poQUQhARewGzA32E%3DwLRMyvun39zd8JiYpJz5yMKaMTkYJzdkQWxIt449j1ySt6bqdk
# API Key: xXYmWiNOMqDsNDkdqWcgJCJ78
# API Key Secret: rMSXkdATyfbMrBbRW7UtikVato9uEtcTcptP8I6Wxf17HsFyeB
# Client ID: djJRc1dxa2stRFpYQXkwcUEtWFQ6MTpjaQ
# Client Secret: ok-Hbqii4yPGObK3DL_alhbE3ZYvSo5U7aLldSwQN0uqZDcCtw

import requests

# Your Bearer Token from the Twitter Developer Dashboard
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAPEOpwEAAAAAVHvsNit2Av0poQUQhARewGzA32E%3DwLRMyvun39zd8JiYpJz5yMKaMTkYJzdkQWxIt449j1ySt6bqdk'


def get_user_id(username):
    """Fetch the user ID for the given username using API v2."""
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "User-Agent": "v2UserLookupPython"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()['data']['id']

def get_full_tweet_text(tweet_id):
    """Fetch the full text of a specific tweet by its ID."""
    url = f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=text,attachments&expansions=attachments.media_keys&media.fields=url"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "User-Agent": "v2TweetLookupPython"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    tweet_data = response.json()['data']
    tweet_text = tweet_data['text']
    
    # Append media URLs if they exist
    if 'attachments' in tweet_data and 'media_keys' in tweet_data['attachments']:
        media_data = response.json().get('includes', {}).get('media', [])
        for media in media_data:
            if media['media_key'] in tweet_data['attachments']['media_keys']:
                tweet_text += f"\n\n{media['url']}"
    
    return tweet_text

def get_latest_tweet_or_thread(user_id):
    """Fetch the latest tweet or the entire thread if the latest tweet is part of one."""
    url = f"https://api.twitter.com/2/users/{user_id}/tweets?tweet.fields=text,conversation_id,attachments,author_id&expansions=attachments.media_keys&media.fields=url&max_results=10&exclude=retweets,replies"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "User-Agent": "v2TweetLookupPython"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    tweets_data = response.json()['data']
    latest_tweet_data = tweets_data[0]
    
    # Fetch the full text of the latest tweet
    full_tweet_text = get_full_tweet_text(latest_tweet_data['id'])
    
    # If the tweet's ID matches its conversation_id, it's part of a thread
    if latest_tweet_data['id'] == latest_tweet_data['conversation_id']:
        # Extract all tweets in the thread authored by the user
        thread_tweets = [tweet['text'] for tweet in tweets_data if tweet['conversation_id'] == latest_tweet_data['conversation_id'] and tweet['author_id'] == user_id]
        return "\n\n".join(thread_tweets)
    else:
        return full_tweet_text

def main():
    """Main function to execute the script."""
    username = input("Enter the Twitter username (without '@'): ")
    user_id = get_user_id(username)
    content = get_latest_tweet_or_thread(user_id)
    
    with open(f"C:\\Users\\Toune\\iCloudDrive\\Documents\\Code\\Thread\\{username}_latest_content.txt", "w", encoding="utf-8") as file:
        file.write(content)
    
    print(f"Latest content from @{username} has been saved to {username}_latest_content.txt")

if __name__ == "__main__":
    main()