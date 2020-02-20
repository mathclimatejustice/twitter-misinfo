import os
import os.path as osp

PACKAGE_DIR = osp.dirname(osp.abspath(__file__))
BASE_DIR = osp.dirname(PACKAGE_DIR)

DEFAULT_DATASET_DIR = osp.join(BASE_DIR, 'datasets')

# creates default data directory if it doesn't exist already
if not osp.exists(DEFAULT_DATASET_DIR):
    os.mkdir(DEFAULT_DATASET_DIR)
