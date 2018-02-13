# Table of Contents
1. [Introduction](README.md#introduction)
2. [Dependencies](README.md#dependencies)
3. [Data Structures](README.md#data-structures)
4. [Process](README.md#process)
5. [Notes](README.md#notes)

# Introduction
This repository is my solution to the Insight Data Engineering Challenge.

The process can be started by running run.sh in a terminal, or alternatively:

python ./src/donation_analytics_driver.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt

in the donation-analytics directory.

# Dependencies

Python 3.6. All of the libraries used are Python standard libraries.

# Data Structures
The two key data structures I used are:

donors: dictionary of previous donors with keys of (name, zip) : year
contributions: dictionary with keys of (cmte_id, zip, year) and values of ContributionData

These data structures are hash tables, which allow for fast retrieval of relevant data.

For donors, since a unique donor is identified by a name and zip-code, a tuple of those two values because a natural choice for the key. The value is the earliest year of any of their previous donation. If a record is streamed in with a year that is earlier than that stored in donors, that means that this isn't a repeat donor and the record can be ignored. However, the year value in donors needs to be updated for future records.

For contributions, a key of tuple (cmte_id, zip, year) uniquely identifies the contributions for a given zip-code for a given year. A nested dictionary was also considered. The key of tuple was chosen in the end because of faster lookup and insertion speed. Having too many keys due to the large number of possible combinations of cmte_id, zip, year was a concern, but reality implies that cmte_id (client politician candidates) would be a few hundred to a few thousand. Possible zip-codes and years are also greatly limited. Therefore, it was assumed that the dictionary will be able to handle the number of keys.

The ContributionData class in contribution_data.py holds a list of historical contributions, used in the calculation of the percentile. This class also keeps track of the running total of contributions. All of the numerical calculations happen using this class.

# Process

The donation_analytics_driver.py file is the main driver and backbone. It calls all of the other functions, which are abstracted away, allowing for easy changes to the specifications and validations.

The input stream uses the Python file object for natural file handling, but a custom stream can be implemented in read_data() that returns an object that implements the IOWrapper interface. 

The general process is as follows:
Read in data
For each line in the data stream,
    validate the record
    check if the donor is a repeat donor
    if so,
        append the record with percentile analysis to the output file


# Notes

Each validation of each field is split into its own function so that if/when specifications change, the validation function can be easily updated.

The bisect module is used to keep the contributions_history list sorted on each insert. This allows for fast percentile calculations. bisect.insort() keeps the list sorted after every insert.