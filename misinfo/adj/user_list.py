"""Script for extracting user names tweet data csv """
import misinfo.file_utils as futils
from misinfo.data_wrangler import get_columns
from misinfo.config_info import DEFAULT_DATASET_DIR


USER_ID = "user.id"
USER_HEADERS = [USER_ID, "user.screen_name", "user.name", "user.followers_count"]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=str, help="path to csv data")
    parser.add_argument("--outfile", type=str, default=None,
                        help="output file (if not provided will generate it)")
    parser.add_argument("-c", type=int, default=250,
                        help="chunk size (number of rows to read in at a time)(default=250)")
    parser.add_argument("-n", type=int, default=None,
                        help="number of chunks to process (default=all chunks)")
    args = parser.parse_args()

    outfile = args.outfile
    if outfile is None:
        outfile_name = f"{futils.get_file_name(args.csv_path)}_USER_NAME_LIST"
        outfile = futils.generate_file_path(DEFAULT_DATASET_DIR, outfile_name, ".csv")

    df = get_columns(args.csv_path, USER_HEADERS, args.c, args.n)
    df = df.drop_duplicates(USER_HEADERS)
    df.to_csv(outfile)
