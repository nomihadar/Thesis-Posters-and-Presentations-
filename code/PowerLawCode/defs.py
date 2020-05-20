import os
import numpy as np
import re
#import matplotlib.pyplot as plt
#import seaborn as sns
import pandas as pd
import scipy, math, random, time, copy, argparse, platform, logging, socket
from subprocess import call
from shutil import copyfile
import shutil

SEP = "/"

if platform.system() == 'Linux':

	PROJECT_PATH = r"/groups/itay_mayrose/danaazouri/powerLawProject/"
	DATA_PATH = os.path.join(PROJECT_PATH, "data")
	SUMMARY_PATH = os.path.join(PROJECT_PATH, "summary_files")
	PROGRAM_PATH = os.path.join(PROJECT_PATH, "Programs")

else:
	if os.path.exists(r"D:\Users\Administrator\Dropbox\PowerLaw"):  # Dana's in lab
		DATA_PATH = r"D:\Users\Administrator\Dropbox\PowerLaw\data\\"
		CODE_PATH = r"D:\Users\Administrator\Dropbox\PowerLaw\code\\"
	elif os.path.exists(r"C:\\Users\\ItayMNB3\\Dropbox\\PowerLaw"): # Dana's laptop
		DATA_PATH = r"C:\\Users\\ItayMNB3\\Dropbox\\PowerLaw\\data\\"
		CODE_PATH = r"C:\\Users\\ItayMNB3\\Dropbox\\PowerLaw\code\\"



#read paths dictionary
LOAD_PATHS = True # flag if load paths
if LOAD_PATHS:
	PATHS_DIC = os.path.join(SUMMARY_PATH, "PATHS_DICTIONARY.csv") #PATHS_DICTIONARY.csv
	df = pd.read_csv(PATHS_DIC,index_col=0)
	DIC = df['path'].to_dict()

#users
NOMI = "nomihadar"
DANA = "danaazouri"

#cols names
REPLICATE_COL = 'replicate'
PATH_COL = 'path'
ID_COL = 'id'

#alignments
FASTA_FORMAT = "fasta"
PHYLIP_FORMAT = "phylip-relaxed"
NEXUS_FORMAT = "nexus"
FASTA_SUFFIX = ".fas"
PHYLIP_SUFFIX = ".phy"
REF_MSA_PHY = "ref_msa.aa.phy"
REF_MSA_FAS = "ref_msa.aa.fas"

#databases
DATA_BASES = ["Selectome", "PANDIT"]

# Simple Indel Code (SIC)
SIC_OUTPUT = "sic_output.csv"
SIC_OUTPUT_WITH = "sic_with_edges.csv"
SIC_OUTPUT_WITHOUT = "sic_without_edges.csv"
COL_NAMES_SIC = \
	["length", "in edge","start position", "end position",
	 "% species found in"]

#tree file
TREE_FILE = "RAxML_bestTree.tree"

#indel model parameters file
INDEL_MODEL_OUTPUT = "indel_model.csv"
COL_NAMES_INDEL_MODEL = ["ir", "a", "rl", "max gap length"]

#simulations with indelible
INDELIBLE_OUTPUT_REG = "sim[0-9]+_TRUE_[0-9]+.phy"
N_SIM = 30
INDELIBLE_TRUE = "sim01_TRUE_{i}.phy"
INDELIBLE_SEQS = "sim01_{i}.fas"

'''
###############
Directories
###############
'''
SIC_DIR = "simple_indel_coding"
SIC_DIR_SIM = "sic_{:02d}" #replicate id
SIMULATIONS_DIR = "simulations01/"

TREE_RAXML_DIR = "tree_raxml"

'''
###############
Messages
###############
'''
NO_INDELS = "No indels"