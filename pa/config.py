#!/usr/bin/env python3

"""Config for voter roll checks. Please make sure these values are correct before running the checker."""

# Point this to the directory containing the FVE files.
data_dir = '../data/pa-statewide/'
data_dir = '../data/PA_Statewide_Voter_Rolls_2020-11-23/PA_Statewide_Voter_Rolls_11-23/'

# format YYYYMMDD, any voter with a DOB less than this will be considered invalid.
min_dob = 19070202

# csv files for invalid voters will go to this directory. one csv file for each reason for invalidation.
# note that some invalid voters can appear in more than 1 file, if they satisfy multiple reasons for invalidation.
# the headers will be the same as those in the FVE files.
output_dir = '/tmp/'

# These parameters are only relevant to election day.
# For example, for election day we would consider someone who registered after election day as invalid.
filter_for_election_day = False
registration_deadline = 20201019 # from: https://www.votespa.com/Register-to-Vote/Pages/default.aspx
election_day = 20201103
