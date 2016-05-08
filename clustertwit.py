#!/usr/bin/pyhton
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Sebastian Garcia. eldraco@gmail.com
"""

# This is a quick hack/implementation for grouping twits based on a special concept of similarity.
#
# We group the twits that have more than N words identical to words in the group.
# If the twit is accepted in a group, its words are added to the group
# Twits are "cleaned":
# - Delete all the words with less than 5 letters. Yes, as you read. (original idea is to get rid of articles. If you know something better, tell me)
# - Delete all the trailing spaces, if there are any
# - Put all the letters in lowercase
# - Delete all the chars ,'!.  This is to consider similar words with these chars at the end.

# To use this software is very useful to tune two thresholds depending on what you want.
# 1. The self.minimum_amount_of_matching_words in the TwitGroup class. 
# This is for controling how many words should be similar to be accepted in a groupa. We found that 2 is ok.
# 2. When showing the final groups, which groups to show. That is controled by counting the amount of twits in the groups.
# The variable minimum_amount_of_twits_to_show_the_group controls that. This is a really a interface issue that should be controled 
# depending on what you want to show to the user.

# To use it, just cat a file with twits and give it as stdin to this program
# Example:
# cat dataset | ./

import re
import sys

twitts_groups=[]
groups_id = 0
verbose = 0
minimum_amount_of_twits_to_show_the_group = 3

class Twit():
    """ Class to hold all the info of one twit"""
    def __init__(self, text):
        self.original_text = text
        self.filtered_text = self.filter(text)
        self.text = self.filtered_text
        self.v_text = self.text.split()
        self.group = False

    def filter(self, text):
        """ Filter the original text to have:
        - Only the words with more than 5 letters
        - Put the words to lowercase
        - Delete the chars '!.
        """
        result = []
        for word in text.split():
            if len(word) > 5:
                result.append(word.lower().strip().replace('\'','').replace('!','').replace('.',''))
        return ' '.join(iter(result))
    
    def __repr__(self):
        return 'Text: {}'.format(self.original_text)

class TwitGroup():
    """ Class to hold a group of twits that are similar """
    def __init__(self, id):
        self.id = id + 1
        self.twits = []
        self.group_words = []
        self.minimum_amount_of_matching_words = 2

    def accept(self, twit):
        """ Receives a twit object and decided if it is accepted in the group or not """
        amount = 0
        # Dont process twits that were already grouped
        if twit.group:
            return False
        if verbose > 2:
            print '\tWords in group: {}'.format(self.group_words)
        for word in twit.v_text:
            if verbose > 3:
                print '\t\tTrying word: {}'.format(word)
            # Check if the current word is in this group
            try:
                if self.group_words.index(word) >= 0:
                    amount += 1
            except ValueError:
                # Not in the list
                pass
        if verbose > 2:
            print '\tFinal amount: {}'.format(amount)
        # If all of the words in the twit matched... dont accept it. So we delete duplicate twits.
        if amount > 0 and amount == len(twit.v_text):
            return False
        # Did we overcome the threshold?
        elif amount >= self.minimum_amount_of_matching_words:
            self.add_twit(twit)
            # Mark the twit as accepted
            twit.group = self.id
            return True
        else:
            return False
   
    def add_twit(self, twit):
        """ Add a twit to this group. It should be accepted before"""
        for word in twit.v_text:
            self.group_words.append(word)
        self.twits.append(twit)
    
    def print_twits(self):
        """ Print all the twits in this group"""
        for twit in self.twits:
            print '\t', twit
            #print twit.filtered_text

    def __repr__(self):
        return 'Group {}. Amount of twits: {}'.format(self.id, len(self.twits))

# 
# Start by reading the lines from stdin
for line in sys.stdin:
    # Avoid empty lines
    newtwit = Twit(line.strip())
    if verbose > 1:
        print 'Processing twit: {}'.format(newtwit.original_text)
    for group in twitts_groups:
        group.accept(newtwit)
    # If the twit was not accepted, create a new group for it
    if not newtwit.group:
        newgroup = TwitGroup(groups_id)
        newgroup.add_twit(newtwit)
        twitts_groups.append(newgroup)
        groups_id += 1

# Print groups
print 
print 'Final Groups:'
for group in twitts_groups:
    if len(group.twits) > minimum_amount_of_twits_to_show_the_group:
        print group
        group.print_twits()

