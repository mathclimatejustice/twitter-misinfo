import twint

test_username = "joetruthb4feels"
test_userid = 1205291211004661760


def get_followers(username, resume=True):
    """Returns df of followers of username and users they are following"""
    save_file = f"../../datasets/{username}_followers.csv"

    c = twint.Config()
    c.Username = username
    c.Pandas = True
    c.Output = save_file
    c.Store_csv = True

    if resume:
        c.Resume = save_file

    print(f"\nGetting followers of {username}")
    twint.run.Followers(c)
    followers_df = twint.storage.panda.Follow_df

    return followers_df


def get_following(username, resume=True):
    """Returns df of followers of username and users they are following"""
    save_file = f"../../datasets/{username}_following.csv"

    c = twint.Config()
    c.Username = username
    c.Pandas = True
    c.Output = save_file
    c.Store_csv = True

    if resume:
        c.Resume = save_file

    print(f"\nGetting following of {username}")
    twint.run.Following(c)
    following_df = twint.storage.panda.Follow_df

    return following_df


def collect_info(username_list):
    """Collect list of followers and following for all usernames in list """
    info = {}
    for username in username_list:
        followers_df = get_followers(username)
        following_df = get_following(username)
        info[username] = followers_df, following_df
    return info


def construct_adj_list(username_list, user_info):
    """Construct adjacency list.
    For each user, there is:
    1. an entry containing all users in username_list that are followers
    2. an entry containing all users in username_list that they are following
    """



if __name__ == "__main__":
    followers_df = get_followers(test_username)
    # following_df = get_following(test_username)

    print(f"\n{'-'*60}\nFollowers:\n{'-'*60}")
    try:
        print(followers_df['followers'][test_username])
    except Exception as ex:
        print(str(ex))

    print(f"\n{'-'*60}\nFollowing:\n{'-'*60}")
    try:
        print(following_df['following'][test_username])
    except Exception as ex:
        print(str(ex))
