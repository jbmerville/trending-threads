from twarc import Twarc2
import json

# Initialize Twarc2 with your Twitter API Bearer Token
t = Twarc2(bearer_token="AAAAAAAAAAAAAAAAAAAAAPEOpwEAAAAAN5Ng6NYpoCUQedux%2F3jyjvSIQ5k%3DwzqkkGP9901Bv9SdeshLGnoWY9Llvjhz4iNQfBBGeLFVXDReEx")

# List of Twitter usernames to track
usernames_to_track = ["culturaltutor", "WineBottleClub"]  # Add usernames here

def get_user_id(username):
    """
    Get the user ID for a given username.
    """
    try:
        users = list(t.user_lookup(users=[username], user_fields=["id"]))
        return users[0]["id"]
    except Exception as e:
        print(f"Error fetching user ID for {username}: {e}")
        return None

def listen_for_tweets(user_ids):
    """
    Listen for new tweets from the list of user IDs and save them to text files.
    """
    for tweet in t.sample():
        # Check if the tweet is from one of the user IDs we're tracking
        if tweet["author_id"] in user_ids.values():
            username = [name for name, id in user_ids.items() if id == tweet["author_id"]][0]
            tweet_text = tweet["text"]
            
            # Append the tweet text to a file
            with open(f"C:\\Users\\Toune\\iCloudDrive\\Documents\\Code\\Thread\\{username}_tweets.txt", "a", encoding="utf-8") as f:
                f.write(tweet_text + "\n\n")
            
            print(f"Appended latest tweet from @{username}")

def main():
    """
    Main function to execute the script.
    """
    # Get user IDs for the usernames we're tracking
    user_ids = {username: get_user_id(username) for username in usernames_to_track}
    user_ids = {k: v for k, v in user_ids.items() if v is not None}  # Filter out None values
    
    # Listen for new tweets from these user IDs
    listen_for_tweets(user_ids)

if __name__ == "__main__":
    main()