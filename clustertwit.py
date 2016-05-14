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

# clustertwit.py
# Author: Sebastian Garcia. eldraco@gmail.com, @eldracote
# Thanks to @verovaleros for the thinking sessions and the creation of the dataset
"""

# clustertwit.py is a quick hack/implementation for grouping twits based on a special concept of similarity.
#
# We group the twits that have more than N words identical to words in the group.
# If the twit is accepted in a group, its words are added to the group
# Twits are "cleaned":
# - Delete all the words with less than 5 letters. Yes, as you read. (original idea is to get rid of articles. If you know something better, tell me)
# - Delete all the trailing spaces, if there are any
# - Put all the letters in lowercase
# - Delete all the chars ,'!.  This is to consider similar words with these chars at the end.

# To use this software is very useful to tune two thresholds depending on what you want.
# 1. The -w parameter controls this. 
# This is for controling how many words should be similar to be accepted in a groupa. We found that 2 is ok.
# 2. When showing the final groups, which groups to show. That is controled by counting the amount of twits in the groups.
# The parameter -t controls that. This is a really a interface issue that should be controled depending on what you want to show to the user.

# Also use the verbose -v parameter to control what you see and some debuging

# To use it, just cat a file with twits and give it as stdin to this program
# Example:
# cat TestDataset | python ./clustertwit.py

# It works in Linux and OSX at least

import sys
import argparse

twitts_groups=[]
groups_id = 0
version = '0.3'

class Twit():
    """ Class to hold all the info of one twit"""
    def __init__(self, text):
        self.original_text = text
        self.filtered_text = self.filter(text)
        self.text = self.filtered_text
        self.v_text = self.text.split()
        self.group = False
        self.duplicate = False

    def filter(self, text):
        """ Filter the original text to have:
        - Only the words with more than 5 letters
        - Put the words to lowercase
        - Delete the chars '!.
        """
        result = []
        for word in text.split():
            if len(word) > 5 and not self.is_blacklisted(word):
                result.append(word.lower().strip().replace('\'','').replace('!','').replace('.',''))
        return ' '.join(iter(result))
    
    def __repr__(self):
        return 'Text: {}'.format(self.original_text)

    def is_blacklisted(self, word):
        blacklist = ['https']
        if any(w in word for w in blacklist):
            return True
        return False
    
    def is_duplicate(self):
        self.duplicate = True


class TwitGroup():
    """ Class to hold a group of twits that are similar """
    def __init__(self, id, min_words):
        self.id = id + 1
        self.twits = []
        self.group_words = []
        self.minimum_amount_of_matching_words = min_words

    def accept(self, twit):
        """ Receives a twit object and decided if it is accepted in the group or not """
        amount = 0
        # Dont process twits that were already grouped
        if twit.group:
            return False
        if args.verbose > 2:
            print '\tWords in group: {}'.format(self.group_words)
        for word in twit.v_text:
            if args.verbose > 3:
                print '\t\tTrying word: {}'.format(word)
            # Check if the current word is in this group
            try:
                if self.group_words.index(word) >= 0:
                    if args.verbose > 2:
                        print '\t\tMatched: {}'.format(word)
                    amount += 1
            except ValueError:
                # Not in the list
                pass
        if args.verbose > 2:
            print '\tFinal amount: {}'.format(amount)
        # If all of the words in the twit matched... dont accept it. So we delete duplicate twits.
        if amount > 0 and amount == len(twit.v_text):
            twit.is_duplicate()
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


####################
# Main
####################
print 'ClusterTwit. Version {}\n'.format(version)

# Parse the parameters
parser = argparse.ArgumentParser()
parser.add_argument('-w', '--words', help='Minimum amount of words in each twit that should be equal to the words in the group.', action='store', default = 2, type=int, required=False)
parser.add_argument('-t', '--twitts', help='Only show the groups with this amount of twitts inside.', action='store', default = 3, required=False, type=int)
parser.add_argument('-v', '--verbose', help='Verbosity.', action='store', default = 1, required=False)
parser.add_argument('-T', '--twitter', help='Use twitter API. See code for keys.', action='store_true', required=False)
args = parser.parse_args()

if args.twitter:
    print 'Getting your tweets to the file twitter-cache.tmp'
    try:
        import tweepy
    except ImportError:
        print 'You need to install the library tweepy. Please do from the git repo https://github.com/tweepy/tweepy, if not it won\'t run'
    from tweepy import OAuthHandler
    # Put Here your keys
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    file = open('./twitter-text-cache.tmp','a+')
    file_all = open('./twitter-cache.tmp','a+')
    for tweet in tweepy.Cursor(api.home_timeline).items(100):
        # Process a single status
        file.write(str(tweet.text.encode('utf-8') + '\n'))
        file_all.write(str(tweet._json))
        print tweet.text
    file.close()
    file_all.close()
else:
    # Start by reading the lines from stdin
    for line in sys.stdin:
        # Avoid empty lines
        newtwit = Twit(line.strip())
        if args.verbose > 1:
            print 'Processing twit: {}'.format(newtwit.original_text)
        for group in twitts_groups:
            group.accept(newtwit)
        # If the twit was not accepted, create a new group for it
        if not newtwit.group and not newtwit.duplicate:
            newgroup = TwitGroup(groups_id, args.words)
            newgroup.add_twit(newtwit)
            twitts_groups.append(newgroup)
            groups_id += 1

    # Print groups
    print 
    print 'Final Groups with more than {} twits.'.format(args.twitts)
    for group in twitts_groups:
        if len(group.twits) > args.twitts:
            print group
            group.print_twits()

