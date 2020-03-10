"""Combines a a dataset of each user and a list of their followers, and
a dataset on user info, into a single data set
"""
import pandas as pd

import misinfo.file_utils as futils
from misinfo.config_info import DEFAULT_DATASET_DIR


USER_ID = "user_id"
USER_NAME = "user.screen_name"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("user_info_csv", type=str, help="path to user info csv data")
    parser.add_argument("follow_tsv", type=str, help="path to follow csv data")
    parser.add_argument("--use_user_name", action="store_true",
                        help="Combine using username, instead of ID")
    parser.add_argument("--outfile", type=str, default=None,
                        help="output file (if not provided will generate it)")
    args = parser.parse_args()

    outfile = args.outfile
    if outfile is None:
        user_info_filename = futils.get_file_name(args.user_info_csv)
        follow_filename = futils.get_file_name(args.follow_tsv)
        common_filename = futils.longest_common_prefix([user_info_filename, follow_filename])
        outfile_name = f"{common_filename}_FOLLOW_DATA"
        outfile = futils.generate_file_path(DEFAULT_DATASET_DIR, outfile_name, ".tsv")

    user_info_df = pd.read_csv(args.user_info_csv)
    follow_df = pd.read_csv(args.follow_tsv, sep="\t")

    join_col = USER_NAME if args.use_user_name else USER_ID
    joined_df = pd.merge(user_info_df, follow_df, on=join_col)
    joined_df.to_csv(outfile, sep="\t")
