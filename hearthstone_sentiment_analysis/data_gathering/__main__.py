from .search import get_tweets_by_users, get_tweets_by_hashtags


def main() -> None:
    with open("data/twitter_users.txt", "r") as f:
        twitter_users = f.read().split()

    # get_tweets_by_users(twitter_users)
    get_tweets_by_hashtags(["Hearthstone", "forgedinthebarrens", "wildhs"])


main()