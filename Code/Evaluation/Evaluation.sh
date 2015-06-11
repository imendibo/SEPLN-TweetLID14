#!/bin/bash

# _____________________________________________________________________________________________
#
#
#         RUN: ./Evaluation.sh <result file NAME> <dataset file NAME> <DESCRIPTION>
#
#            Inputs:
#                   result file NAME = only name without .txt
#                   dataset file NAME = only name without .txt
#                   DESCRIPTION = brief description of the obtained results
#
#
#             Evaluation result will be stored in Evaluation folder name as the description.
#             Result file will move to a folder name as the description.
#
# _____________________________________________________________________________________________

RESULT_NAME=$1
DATASET_NAME=$2
DESCRIPTION=$3

RESULT_PATH='../../Results/'$1'.txt'
DATASET_PATH='../../Dataset/'$2'.tsv'

FOLDER='../../Evaluation/'$DESCRIPTION
mkdir $FOLDER

echo 'Folder '$FOLDER' created.'

EVALUATION_PATH=$FOLDER'/'$1'_'$2'.txt'

perl tweetLID_eval.pl -d $RESULT_PATH -r $DATASET_PATH -> $EVALUATION_PATH

mkdir '../../Results/'$DESCRIPTION

mv $RESULT_PATH '../../Results/'$DESCRIPTION'/'

echo 'Done'