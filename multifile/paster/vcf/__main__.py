import argparse

from multifile.paster.vcf.paster import VCFPaster


def main():
    parser = argparse.ArgumentParser(description="Merge VCF horizontally.")
    parser.add_argument('input_paths', type=str, nargs='+', help="paths to files to merge")
    parser.add_argument('output_path', type=str, help="path to output file")
    parser.add_argument('-d', '--delimeter', type=str, default='\t', help="delimeter")
    parser.add_argument('-b', '--batch-size', type=int, default=999, help='size of each input batch to process one at a time')
    parser.add_argument('--n-header-lines', type=int, default=11, help="number of header lines (will be read only once)")
    parser.add_argument('--n-fixed-cols', type=int, default=9, help="number of fixed columns on the left")
    parser.add_argument('--n-samples-each', type=int, default=1, help="number of samples each input file")
    parser.add_argument('-t', '--temp-dir-path', type=str, help="path to directory for storing temporary files while pasting")
    args = parser.parse_args()

    paster = VCFPaster(args.input_paths, args.output_path, args.delimeter, args.batch_size,
                        args.n_header_lines, args.n_fixed_cols, args.n_samples_each, args.temp_dir_path)
    paster.paste()


if __name__ == '__main__':
    main()
