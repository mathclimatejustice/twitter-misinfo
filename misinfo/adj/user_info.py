import misinfo.file_utils as futils
from misinfo.data_wrangler import get_columns
from misinfo.config_info import DEFAULT_DATASET_DIR


USER_HEADERS = [
    "user.contributors_enabled", "user.created_at", "user.default_profile", "user.default_profile_image",
    "user.description", "user.favourites_count", "user.follow_request_sent", "user.followers_count",
    "user.following", "user.friends_count", "user.geo_enabled", "user.id", "user.id_str", "user.is_translator",
    "user.lang", "user.listed_count", "user.location", "user.name", "user.notifications",
    "user.profile_background_color", "user.profile_background_image_url", "user.profile_background_image_url_https",
    "user.profile_background_tile", "user.profile_banner_url", "user.profile_image_url", "user.profile_image_url_https",
    "user.profile_link_color", "user.profile_sidebar_border_color", "user.profile_sidebar_fill_color",
    "user.profile_text_color", "user.profile_use_background_image", "user.protected", "user.screen_name",
    "user.statuses_count", "user.time_zone", "user.translator_type", "user.url", "user.utc_offset", "user.verified"
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
    df.to_csv(outfile)
