import datetime

def validate_cmte_id(id):
    return id

def validate_other_id(id):
    return not id

def validate_date(date):
    """
    Delegate the date validation to the datetime library.

    :param date: date to be validated
    :type date: str
    :returns: datetime if true, else False
    """
    try:
        return datetime.datetime.strptime(date, '%m%d%Y')
    except ValueError:
        return False

def validate_zip(zip):
    return len(zip) >= 5 and zip.isdigit()

def validate_name(name):
    return name

def validate_amount(amount):
    return amount

def validate_record(record):
    """
    Validate that the input string representing a record is well-formed and valid.

    :param record: record with contribution data
    :type record: string
    :returns: dictionary with values of interest: cmte_id, name, zip, year, amount
    :rtype: dict
    """
    record = record.split('|')

    # If any validation fails, ignore this record by returning None
    # not (X and Y and Z) is equivalent to not X or not Y or not Z
    if not (validate_other_id(record[15]) and
            validate_cmte_id(record[0]) and
            validate_date(record[13]) and
            validate_zip(record[10]) and
            validate_name(record[7]) and
            validate_amount(record[14])):
        return None

    record_dict = {
        'cmte_id' : record[0],
        'name' : record[7],
        'zip' : record[10][:5],
        'year' : record[13][-4:],
        'amount' : float(record[14])
    }

    return record_dict