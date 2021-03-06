"""Script for extracting user info from all tweet data csv """
import misinfo.file_utils as futils
from misinfo.data_wrangler import get_columns
from misinfo.config_info import DEFAULT_DATASET_DIR

USER_ID = "user.id_str"
USER_HEADERS = [
    "user.created_at", "user.follow_request_sent", "user.followers_count",
    "user.following", "user.friends_count", USER_ID,
    "user.location", "user.name", "user.screen_name",
    "user.statuses_count", "user.time_zone"
]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=str, help="path to csv data")
    parser.add_argument("--outfile", type=str, default=None,
                        help="output file (if not provided will generate it)")
    parser.add_argument("-c", type=int, default=10000,
                        help="chunk size (number of rows to read in at a time)(default=10000)")
    parser.add_argument("-n", type=int, default=None,
                        help="number of chunks to process (default=all chunks)")
    args = parser.parse_args()

    outfile = args.outfile
    if outfile is None:
        outfile_name = f"{futils.get_file_name(args.csv_path)}_USER_INFO"
        outfile = futils.generate_file_path(DEFAULT_DATASET_DIR, outfile_name, ".csv")

    df = get_columns(args.csv_path, USER_HEADERS, args.c, args.n)
    df = df.drop_duplicates(USER_ID)
    df.to_csv(outfile)
