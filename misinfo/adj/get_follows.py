"""Given a list of users, scrapes the users followers and following

Input file should contain the following headers (at minimum):
1. 'user.id' - this column contains the user ID of each target user
2. 'user.followers_count' - the number of follwers the user has

"""
import time
import twint
import random
import pandas as pd

import misinfo.file_utils as futils
from misinfo.config_info import DEFAULT_DATASET_DIR

FOLLOW_RESULT_COLUMN = 'username'
USERNAME_COLUMN = "user.screen_name"
USERID_COLUMN = "user.id"
FOLLOWER_COUNT_COLUMN = "user.followers_count"
FOLLOWING_COUNT_COLUMN = "user.friends_count"


def get_follow(user, get_followers, target_count=None, use_user_id=False, retries=3, retry_sleep_period=3):
    """Returns df of followers of username (followers=True) or users they are following
    (followers=False)

    Arguments
    ---------
    user : str
        the user (either username or userid)
    get_followers : bool
        If true will scrape for followers, if false will scrape for following
    target_count : int
        how many followers/following you expect. If given then will retry scraping until the
        target is met. If None then will not retry once scraping call returns.
    retries : int
        the number of time scraping will be tried until target count is met (default=3)

    Returns
    -------
    follows : list
        list followers
    target_met : bool
        true if target count was met
    """
    c = twint.Config()
    if use_user_id:
        c.User_id = user
    else:
        c.Username = user
    c.Pandas = True

    scrape_fn = twint.run.Followers if get_followers else twint.run.Following
    target_met = False
    tries = 0

    f_key = 'followers' if get_followers else 'following'
    follower_list = None
    while not target_met and tries < retries:
        tries += 1
        print(f"  Try {tries} of {retries}")
        try:
            scrape_fn(c)
            df = twint.storage.panda.Follow_df
            follower_list = df[f_key].tolist()[0]
            print(len(follower_list), target_count)
            if target_count is None or len(follower_list) >= target_count:
                target_met = True
        except Exception as ex:
            print(f"Exception while scrapping: {str(ex)}")

        # add some randomness, to hopefully help fool twitter
        sleep_period_min = min(0.5, retry_sleep_period-2)
        sleep_period_max = max(1, retry_sleep_period+2)
        time.sleep(random.uniform(sleep_period_min, sleep_period_max))

    if follower_list is not None:
        scrape_count = len(follower_list)
        print(f"  Finished scraping. Total scraped={scrape_count}, target met={target_met}")
    else:
        follower_list = ["NA"]
        print(f"   Unable to scrape followers after {retries} attempts.")

    return follower_list, target_met


def collect_info(user_info, get_followers, outfile, use_user_id):
    """Collect list of followers and following for all usernames in user info dataframe

    Arguments
    ---------
    user_info : DataFrame
        dataframe containing user info for target users
    get_followers : bool
        If true will scrape for followers, if false will scrape for following
    outfile : str
        filepath where results will be written
    use_user_id : bool
        use userid instead of username
    """
    follow_column = "followers" if get_followers else "following"
    headers = ["user", follow_column, "target_met"]
    with open(outfile, "w") as fout:
        fout.write("\t".join(headers) + "\n")

    follow_df_key = FOLLOWER_COUNT_COLUMN if get_followers else FOLLOWING_COUNT_COLUMN
    user_key = USERID_COLUMN if use_user_id else USERNAME_COLUMN
    user_list = user_info[user_key].unique()

    print(f"Scraping followers/following for {len(user_list)} users")
    for i, user in enumerate(user_list):
        print(f"\n{'-'*60}\nUser {i} of {len(user_list)}: {user}\n{'-'*60}\n")
        user_df = user_info[user_info[user_key] == user]

        try:
            target_count = user_df[follow_df_key].tolist()[0]
            print(target_count)
        except Exception:
            target_count = None

        follow_list, target_met = get_follow(user, get_followers, target_count, use_user_id)
        row = [str(user), ",".join(follow_list), str(target_met)]
        with open(outfile, "a") as fout:
            fout.write("\t".join(row) + "\n")
        time.sleep(random.uniform(0.05, 1))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=str, help="path to csv data")
    parser.add_argument("--use_user_id", action="store_true",
                        help="Search using user ID, instead of username")
    parser.add_argument("--get_followers", action="store_true", help="Get followers of userlist")
    parser.add_argument("--get_following", action="store_true", help="Get followers of userlist")
    parser.add_argument("--outfile", type=str, default=None,
                        help="output file (if not provided will generate it)")
    args = parser.parse_args()
    assert not (args.get_followers and args.get_following), \
        "Cannot get followers and following (please choose one)"
    assert not (not args.get_followers and not args.get_following), \
        "Must choose either get followers or  get following"

    outfile = args.outfile
    follow = "FOLLOWER" if args.get_followers else "FOLLOWING"
    if outfile is None:
        outfile_name = f"{futils.get_file_name(args.csv_path)}_{follow}_LIST"
        outfile = futils.generate_file_path(DEFAULT_DATASET_DIR, outfile_name, ".tsv")

    user_info = pd.read_csv(args.csv_path)
    collect_info(user_info, args.get_followers, outfile, args.use_user_id)
