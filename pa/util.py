#!/usr/bin/env python3

import csv
import os

LAST_NAME_INDEX = 2
FIRST_NAME_INDEX = 3
MIDDLE_NAME_INDEX = 4

VOTER_STATUS_INDEX = 9
PARTY_INDEX = 11

ELECTION_METHOD = 84
ELECTION_PARTY = 85

def writecsv(file_path, rows):
    w = csv.writer(open(file_path, 'w'), delimiter='\t', quoting=csv.QUOTE_ALL)
    w.writerows(rows)

def readcsv(file_path):
    return csv.reader(open(file_path, 'r'), delimiter='\t')

def votes_by_county():
    rows = csv.reader(open('../data/pa_votes_by_county.csv', 'r'))
    header = next(rows)
    counties = {}
    for r in rows:
        county = {}
        for i in range(1, len(header)):
            county[header[i]] = int(r[i])
        counties[r[0]] = county
    return counties

def party_registration(rows):
    """Returns a count of party registrations."""
    results = {}
    for r in rows:
        if r[VOTER_STATUS_INDEX] != 'A':
            continue
        party = r[PARTY_INDEX]
        if results.get(party) is None:
            results[party] = 0
        results[party] += 1
    return results

def count_rows(rows):
    entries = 0
    for row in rows:
        entries += 1
    print(entries)

def get_fve_files(file_dir):
    """returns map of county name to FVE file."""
    files = os.listdir(file_dir)
    return [file_dir + '/' + x for x in files if ' FVE ' in x]

def get_fve_file_map(file_dir):
    """returns map of county name to FVE file."""
    files = os.listdir(file_dir)
    files = [x for x in files if ' FVE ' in x]
    bycounty = {}
    for f in files:
        bycounty[f.split()[0]] = file_dir + '/' + f
    return bycounty

def sum_dict(d, key_prefix=None):
    s = 0
    for k in d:
        if key_prefix:
            if k[:len(key_prefix)] != key_prefix:
                continue
        s += d[k]
    return s

if __name__ == '__main__':
    """Just some tests."""
    counties = votes_by_county()
    files = get_fve_file_map('../data/pa-statewide/')
    headers = ['county', 'votes / active voters', 'dem votes / registered dems', 'rep votes / registered reps', 'registered dems / registered reps', 'dem votes / rep votes', 'other registrations / active voters']
    output_rows = []
    for c in counties:
        f = files[c]
        rows = readcsv(f)
        p = party_registration(rows)
        cc = counties[c]
        tot_vot = sum_dict(cc)
        tot_reg = sum_dict(p)
        dem_votes = sum_dict(cc, 'biden_')
        rep_votes = sum_dict(cc, 'trump_')
        other_reg = tot_reg - p['D'] - p['R']
        row = [c, tot_vot / tot_reg, dem_votes / p['D'], rep_votes / p['R'], p['D'] / p['R'], dem_votes / rep_votes, other_reg / tot_reg]
        print(row)
        output_rows.append(row)
    with open('/tmp/ratios.csv', 'w') as f:
        f.write(','.join(headers))
        for r in output_rows:
            f.write('\n')
            f.write(','.join([str(x) for x in r]))

