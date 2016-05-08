# clustertwit
Clustertwit is a quick hack/implementation for grouping twits based on a special concept of similarity.

We group the twits that have more than N words identical to words in the group.
If the twit is accepted in a group, its words are added to the group
Twits are "cleaned":

- Delete all the words with less than 5 letters. Yes, as you read. (original idea is to get rid of articles. If you know something better, tell me)
- Delete all the trailing spaces, if there are any
- Put all the letters in lowercase
- Delete all the chars ,'!.  This is to consider similar words with these chars at the end.

## Tunning the thresholds
To use this software is very useful to tune two thresholds depending on what you want.

1. The self.minimum_amount_of_matching_words in the TwitGroup class. 
    This is for controling how many words should be similar to be accepted in a groupa. We found that 2 is ok.
2. When showing the final groups, which groups to show. That is controled by counting the amount of twits in the groups.
    The variable minimum_amount_of_twits_to_show_the_group controls that. This is a really a interface issue that should be controled depending on what you want to show to the user.

Also use the verbose variable to control what you see and some debuging

## Usage
To use it, just cat a file with twits and give it as stdin to this program
Example:
cat TestDataset | python ./clustertwit.py

It works in Linux and IOSX at least
