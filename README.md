# clustertwit
Clustertwit is a quick hack/implementation for grouping twits based on a special concept of similarity.

We group the twits that have more than N words identical to words in the group.
If the twit is accepted in a group, its words are added to the group
Twits are "cleaned":

- Delete all the words with less than 5 letters. Yes, as you read. (original idea is to get rid of articles. If you know something better, tell me)
- Delete all the trailing spaces, if there are any
- Put all the letters in lowercase
- Delete all the chars ,'!.  This is to consider similar words with these chars at the end.
- It implements a simple blacklist of words, to stop things like 'https' to group.

## Tunning the thresholds
To use this software is very useful to tune two thresholds depending on what you want.

1. The amount of words in each twitt that should be equal to the words in a group. The parameter -w.  
    We found that 2 is ok for a small amount of twits. You may need a higher value.
2. When showing the final groups, which groups to show. That is controled by counting the amount of twits in the groups.
    The parameter -t controls that. This is a really a interface issue that should be controled depending on what you want to show to the user.

Also use the verbose -v parameter to control what you see and some debuging

## Twitter API
If you run the program with -T (and you put your API keys in the code) you can download your own tweets and store them on disk. Then you just use that file as your tweets files.

    python ./clustertwit.py -T
    cat twitter-text-cache.tmp | python ./clustertwit.py

## Usage
To use it, just cat a file with twits and give it as stdin to this program
Example:
cat TestDataset | python ./clustertwit.py

It works in Linux and OSX at least

# Authors
This program was done by Sebastian Garcia, eldraco@gmail.com (@eldracote). Thanks to @verovaleros for the thinking sessions and the creation of the dataset.
