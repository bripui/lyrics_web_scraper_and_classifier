import sys
import argparse
import pickle
import time

from typing import Text


# 1. initialize the parser
parser = argparse.ArgumentParser(description='predicts, wether your song text snipped is from Lady Gaga or Red Hot Chili Peppers')

# 2. define command line arguments
parser.add_argument('model', help='choose your model')
parser.add_argument('text', nargs='+', help='your song text snipped')


# 3. read the arguments from the command line
args = parser.parse_args()

X_test = args.text

with open(args.model, 'rb') as file:
    model = pickle.load(file)

y_pred = model.predict(X_test)
print('oh... hmmm...')
time.sleep(1)
print('....')
time.sleep(1)
print('....')
time.sleep(1)
print('wait...')
time.sleep(0.5)
print('....')
time.sleep(0.5)
print('....')
time.sleep(0.5)
print('now i know!')
time.sleep(1)
print(y_pred[0].upper()+'!!!!')