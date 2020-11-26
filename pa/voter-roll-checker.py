#!/usr/bin/env python3

import util
import config

DOB_INDEX = 7
REGISTRATION_DATE_INDEX = 8
VOTER_STATUS_INDEX = 9
STATUS_CHANGE_DATE_INDEX = 10
HOUSE_NUMBER_INDEX = 13
STREET_NAME_INDEX = 14
CITY_INDEX = 17
RESIDENTIAL_STATE_INDEX = 18
RESIDENTIAL_ZIP_CODE_INDEX = 19
LAST_VOTE_DATE_INDEX = 25

total_voters = 0
total_voters_active = 0

# list holding voters with invalid ages.
invalid_dob = []
invalid_dob_active = []
invalid_registration_date = []
invalid_registration_date_active = []
invalid_residential_address = []
invalid_residential_address_active = []

# to check for non-duplicate IDs.
voter_ids = set()

def normalize_date(dob):
    """Converts date in format MM/DD/YYYY to YYYYMMDD, for easier sorting.
        If DOB is invalid, None is returned.
    """
    split = dob.split('/')
    if (len(split) != 3):
        return None
    return split[-1] + split[0] + split[1]

def is_invalid_dob(row):
    """Returns true if voter represented by row is:
        1. too old to be valid
        2. formatted incorrectly
    """
    dob = normalize_date(row[DOB_INDEX])
    if dob is None:
        return True
    dob = int(dob)
    if config.filter_for_election_day and dob > config.election_day - 180000:
        return True
    return dob < config.min_dob

def is_invalid_registration_date(row):
    """Returns true if voter registration date is:
        1. before voter was 18 years old
        2. formatted incorrectly
        3. after election day
    """
    rd = normalize_date(row[REGISTRATION_DATE_INDEX])
    if rd is None:
        return True
    rd = int(rd)

    dob = normalize_date(row[DOB_INDEX])
    if dob is not None:
        dob = int(dob)
        if rd < dob + 140000: # set registration cutoff at 14 yo, because some places allow you to regsiter if you will be 18 by general election day.
            return True

    last_vote_date = normalize_date(row[LAST_VOTE_DATE_INDEX])
    if last_vote_date is not None:
        last_vote_date = int(last_vote_date)
        if last_vote_date < rd:
            return True
        if dob is not None:
            if last_vote_date < dob + 180000:
                return True

    if config.filter_for_election_day and rd > config.registration_deadline:
        return True
    return False

def is_invalid_residential_address(row):
    """Returns true if voter zip code or state is:
        1. empty
        2. formatted incorrectly
    Returns true if city, street name, or house number are blank.
    """
    # zip code
    z = row[RESIDENTIAL_ZIP_CODE_INDEX].strip()
    if not z:
        return True
    z = z.replace('-', '')
    z = z.replace(' ', '')
    if len(z) not in (5, 9):
        return True
    # state
    s = row[RESIDENTIAL_STATE_INDEX].strip()
    if not s:
        return True
    if s.lower() != 'pa':
        return True
    return False


def check_voters(file_path):
    global invalid_dob
    global total_voters
    global total_voters_active
    global voter_ids
    rows = util.readcsv(file_path)
    for r in rows:
        total_voters += 1
        active = r[VOTER_STATUS_INDEX] == 'A'
        voter_id = r[0]
        if not voter_id:
            print('Empty voter ID!', r)
        elif voter_id in voter_ids:
            print('Duplicate voter ID!', r)
            voter_ids.add(voter_id)

        if active:
            total_voters_active += 1
        # dob
        if is_invalid_dob(r):
            invalid_dob.append(r)
            if active:
                invalid_dob_active.append(r)
        # registration date
        if is_invalid_registration_date(r):
            invalid_registration_date.append(r)
            if active:
                invalid_registration_date_active.append(r)
        # residential address
        if is_invalid_residential_address(r):
            invalid_residential_address.append(r)
            if active:
                invalid_residential_address_active.append(r)

if __name__ == '__main__':
    fve_files = util.get_fve_files(config.data_dir)
    for f in fve_files:
        check_voters(f)
    print(f'total registered voters: {total_voters}')
    print(f'total registered active voters: {total_voters_active}')

    print(f'invalid ages: {len(invalid_dob)}')
    print(f'invalid ages, active voters: {len(invalid_dob_active)}')
    util.writecsv(config.output_dir + '/invalid_dob.csv', invalid_dob)

    print(f'invalid registration dates: {len(invalid_registration_date)}')
    print(f'invalid registration dates, active voters: {len(invalid_registration_date_active)}')
    util.writecsv(config.output_dir + '/invalid_registration_date.csv', invalid_registration_date)

    print(f'invalid residential addresses: {len(invalid_residential_address)}')
    print(f'invalid residential addresses, active voters: {len(invalid_residential_address_active)}')
    util.writecsv(config.output_dir + '/invalid_residential_address.csv', invalid_residential_address)


