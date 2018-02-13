import argparse
import os
from donation_analytics_validations import *
from donation_analytics_process import *

def main():
    # Parses command line arguments for the paths
    parser = argparse.ArgumentParser(description='Parses the path for the percentile file and the contributions file.')
    parser.add_argument('contributions_path')
    parser.add_argument('percentile_path')
    parser.add_argument('output_path')
    args = parser.parse_args()

    # If the repeat_donors.txt already exists, remove it first
    try:
        os.remove(args.output_path)
    except OSError:
        pass

    percentile = read_percentile(args.percentile_path)
    input_stream = read_data(args.contributions_path)

    donors = {}
    contributions = {}

    for line in input_stream:
        record = validate_record(line)

        if not record:
            continue

        record = check_repeat_donor(record, donors)

        if record:
            update_contributions(record, contributions)
            result = generate_result(record, contributions, percentile)
            write_output(args.output_path, result)

    input_stream.close()

if __name__ == '__main__':
    main()