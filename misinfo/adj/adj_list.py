"""Given a dataset containing user info and follow data, constructs an
adjacency list dataset, such that for each user, there is a list which
contains the users they follow that are also in the dataset
"""
import pandas as pd
from pprint import pprint

import misinfo.file_utils as futils
from misinfo.config_info import DEFAULT_DATASET_DIR


USER_ID = "user_id"
USER_NAME = "username"
FOLLOW_KEY = "followers"


def get_follower_set(df, username):
    username_df = df[df[USER_NAME] == username].iloc[0]
    raw = username_df[FOLLOW_KEY]
    if isinstance(raw, str):
        return set(raw.split(","))
    else:
        return set()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("follow_data_tsv", type=str, help="path to dataset")
    parser.add_argument("--outfile", type=str, default=None,
                        help="output file (if not provided will generate it)")
    args = parser.parse_args()

    outfile = args.outfile
    if outfile is None:
        outfile_name = f"{futils.get_file_name(args.follow_data_tsv)}_FOLLOW_ADJ_LIST"
        outfile = futils.generate_file_path(DEFAULT_DATASET_DIR, outfile_name, ".tsv")

    df = pd.read_csv(args.follow_data_tsv, sep="\t")

    adj_map = dict()
    all_usernames = df[USER_NAME].unique()

    for username in all_usernames:
        adj_map[username] = {"follower": [], "following": []}

    for username in all_usernames:
        user_followers = get_follower_set(df, username)
        for otheruser in all_usernames:
            if otheruser in user_followers:
                adj_map[username]["follower"].append(otheruser)
                adj_map[otheruser]["following"].append(username)

    pprint(adj_map)
