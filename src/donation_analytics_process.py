from contribution_data import *
from math import ceil, floor

def read_percentile(path):
    """
    Read the percentile number from the given path.

    :param path: path of the file with percentile data
    :param type: str
    :returns: value of percentile
    :rtype: int
    """
    with open(path, 'r') as f:
        return int(f.readline().strip())

def read_data(path):
    """
    Read the contributions data from the given path.
    Returns a File object for streaming, so must be manually closed

    :param path: path of the file with contributions data
    :param type: str
    :returns: the File object
    :rtype: File object
    """
    return open(path, 'r')

def check_repeat_donor(record, donors):
    """
    Check whether or not the donor associated with the record has donated before.

    :param record: dictionary with values of interest: cmte_id, name, zip, year, amount
    :param donors: history of previous donors with keys of (name, zip) : year
    :type record: dict of str : str
    :type donors: dict of (str, str) : str
    :returns: the same record if it is a repeat donor else None
    :rtype: dict
    """
    # If first time seen this donor or current donor contributed earlier than last recorded contribution,
    # store the record and ignore
    if (record['name'], record['zip']) not in donors:
        donors[(record['name'], record['zip'])] = record['year']
        return None
    elif donors[(record['name'], record['zip'])] > record['year']:
        donors[(record['name'], record['zip'])] = record['year']
        return None
    else:
        return record

def update_contributions(record, contributions):
    """
    Update the contributions dictionary with a repeat donor record.
    The ContributionData object will be updated with the new contribution.

    :param record: dictionary with values of interest: cmte_id, name, zip, year, amount
    :param contributions: dictionary with keys of (cmte_id, zip, year) and values of ContributionData
    :type record: dict of str : str
    :type contributions: dict of (str, str, str) : ContributionData
    """
    data = ContributionData()
    if (record['cmte_id'], record['zip'], record['year']) not in contributions:
        contributions[(record['cmte_id'], record['zip'], record['year'])] = data
    else:
        data = contributions[(record['cmte_id'], record['zip'], record['year'])]

    data.add_contribution(record['amount'])
    data.running_total += record['amount']

def generate_result(record, contributions, percentile):
    """
    Generate the result string to be written to output file.
    The result percentile and running_total are both rounded to nearest whole number

    :param record: dictionary with values of interest: cmte_id, name, zip, year, amount
    :param contributions: dictionary with keys of (cmte_id, zip, year) and values of ContributionData
    :param percentile: read in from percentile.txt
    :type record: dict of str : str
    :type contributions: dict of (str, str, str) : ContributionData
    :type percentile: int
    :returns: result for current record with repeat donor
    :rtype: str
    """
    data = contributions[(record['cmte_id'], record['zip'], record['year'])]

    percentile_value = data.calculate_percentile(percentile)
    percentile_value = ceil(percentile_value) if percentile_value % 1 >= 0.5 else floor(percentile_value)

    running_total = data.running_total
    running_total = ceil(running_total) if running_total % 1 >= 0.5 else floor(running_total)

    result = [record['cmte_id'], record['zip'], record['year'], str(percentile_value), str(running_total), str(data.total_transactions())]

    return '|'.join(result) + '\n'

def write_output(path, result):
    """
    Take result string and write it to the specified path.

    :param path: path that the output file will be written to
    :param result: result that will be appended to the output file
    :type path: str
    :type result: str
    """
    with open(path, 'a') as f:
        f.write(result)