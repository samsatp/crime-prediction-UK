from data_prep import create_base_map

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--func', type=str, required=True)
args = parser.parse_args()

if __name__ == '__main__':
    if args.name.lower() == 'createbasemap':
        create_base_map.create_base_map()
