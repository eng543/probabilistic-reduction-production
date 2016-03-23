Project: probabilistic-reduction-production

# Python and R scripts for design and analysis of dissertation experiment

The goal of this project is to investigate how an individual's experience with a language
shapes the way they say words in that language.

Speech varies from moment to moment; if you repeat a word several times, no two instances will 
be precisely the same. Linguists call this phonetic variation. Phonetic variation is conditioned 
by a number of factors, including inter-speaker and intra-speaker factors. 
This project considers one factor from each category. 

The inter-speaker factor of interest is the language background of the speaker. Perhaps unsurprisingly, 
the speech produced by native (L1) and non-native (L2) speakers of a language differ in a 
number of ways. In particular, L2 speakers tend to produce overall slower speech, with 
longer word durations on average compared to L1 speakers.

The intra-speaker factor of interest is the probability of the target word in the current 
context. When a speaker produces a word once, that word is likely to be produced again (it becomes 
a high probability word). Previous research has found that words with high probability tend 
to be shorter in duration on average than words with low probability. In particular, a repeated word 
will have reduced duration compared to the same word produced for the first time. This effect has been
well established for L1 speakers of a language.

The current study considers the interaction of these two factors: do L1 and L2 speakers reduce 
repeated words to the same degree? In this study, L1 and L2 speakers saw a set of pictures. In a trial,
the pictures were animated to rotate, shrink, fade, or expand. Speakers were instructed to describe 
the actions in a statement such as, "The candle rotates." In "repeated" trials, one picture underwent
two actions, so that the second description would include a now high probability word. The dependent variable 
of interest was the duration (in ms) of the target word.

The following results were found:
* L2 speakers produced overall longer word durations on average than L1 speakers (inter-speaker variability)
* Repeated words had overall shorter word durations on average than non-repeated words (intra-speaker variability)
* No significant difference in degree of repetition reduction between L1 and L2 speakers

These results reveal that an individual's linguistic experience shapes production of that language 
in some ways, but not others. While L2 speakers produced longer word durations overall, variation 
in the probabilities of words had a similar effect on word durations as for L1 speakers. These 
results reveal that probabilistic processes are at play during L2 linguistic processing, which 
is an open area of inquiry in the field of linguistics.


# Materials
This repository contains:
* 'Design_Scripts': Directory with Python scripts and necessary files to create pseudo-randomized stimulus lists for running experiment in Max/MSP
* 'Analysis_Scripts': Directory with R markdown file summarizing one set of analyses for this experiment. (Note: all participants consented to sharing of data with general public)


## Design_Scripts
This directory contains a program, which runs three scripts used to create pseudo-randomized stimulus lists (run in order):
Program: makeListProgram.py

Runs following scripts:
* makeStimulusList1.py
* modifyReferenceSheets.py
* makeOtherStimulusLists.py

### Script 1: makeStimuluslist1.py
Creates initial stimulus list with the following structure:
* Four blocks
* Paired items (e.g., arch from pairs1.txt and arm from pairs2.txt) do not appear in same block (block1A/2A and block1B/2B, respectively)
* Repeated and non-repeated conditions for a target do not appear in same block (e.g., arch repeated in block1A, arch non-repeated in block2A)
* 24 target trials (12 repeated, 12 non-repeated) and 12 filler trials (all non-repeated) per block
* Each block has 4 length-2 trials, 16 length-3 trials, 16 length-4 trials
* Filler trials have 2-4 events, target trials have 3 or 4

The list itself must have the following format for Max/MSP:
* One trial per row (total: 144 trials + 6 practice trials)
* Structure: trialLength;picture1 action1;picture2 action2;picture3 action3;picture4 action4;competitorPicture
* Actions never repeated within a trial

This script creates an initial list that will then be modified to create 7 other lists to counterbalance the following factors:
* Position of target item: Block 1A, Block1B, Block2A, Block 2B (which, in turn, counterbalances presentation of repeated vs. non-repeated conditions)
* Trial length assigned to target item: 3 or 4

Finishes by creating a reference sheet for the order of conditions and trial lengths assigned to target items in initial list.

### Script 2: modifyReferenceSheets.py
Creates reference sheets for 7 other counterbalanced lists using the reference sheet created for the initial stimulus list. 

Reference sheets saved in 'reference' directory.

### Script 3: makeOtherStimulusLists.py
Creates full set of final stimulus lists:
* 8 counterbalanced lists
* 3 versions of each list with trials randomized within block
* 6 practice trials included
* 24 total lists

Final stimulus lists saved in 'stimulusLists' directory.

## Analysis_Scripts
This directory contains an overview of one set of analysis for this experiment (html generated from an R markdown file). 
(Note: if html file too big to load, download .zip version, save raw code as .html and reopen, or follow this link: http://rpubs.com/egustafson/noun_duration_analysis).

The analysis includes three steps:
* Pre-processing of raw data
* Data visualization
* Regression modeling

Contact the author for data and executable scripts.
