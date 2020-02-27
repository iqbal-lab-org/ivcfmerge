import argparse

from ivcfmerge import ivcfmerge_batch

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch-size', type=int)
    parser.add_argument('--temp-dir', type=str)
    parser.add_argument('input_paths_file', type=str)
    parser.add_argument('output_path', type=str)
    args = parser.parse_args()

    with open(args.input_paths_file, 'r') as input_paths_file:
        input_paths = input_paths_file.read().splitlines()
        ivcfmerge_batch(input_paths, args.output_path, args.batch_size, args.temp_dir)
