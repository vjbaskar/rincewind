import sys
import os
import pandas as pd



filename = "input.txt"
sample = pd.read_csv(filename, sep="\t", header= None)
sample.columns = ['expt','name','cond','colour']