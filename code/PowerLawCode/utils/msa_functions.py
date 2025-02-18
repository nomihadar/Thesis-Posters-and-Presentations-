import sys, os
from Bio import AlignIO

__author__ = 'Dana'

sys.path.append(os.path.dirname(sys.path[0]))

from defs import *

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line:
		return FASTA_FORMAT
	return PHYLIP_FORMAT

def get_msa_from_file(msa_file_path):
	#open file if exists
	if not os.path.exists(msa_file_path):
		return None
	try:
		msa_format = get_foramt(msa_file_path)
		msa = AlignIO.read(msa_file_path, msa_format)
	except:
		return None
	return msa


def get_msa_properties(msa):
	"""
	:param msa: bio.AlignIO format or path to msa file
	:return:
	"""
	if isinstance(msa, str):
		msa = get_msa_from_file(msa)
	ntaxa = int(len(msa))
	nchars = int(msa.get_alignment_length())

	return ntaxa, nchars

def get_num_indel_blocks(msa):

	if isinstance(msa, str):
		msa = get_msa_from_file(msa)

	gaps_lengths = []
	for record in msa:
		sequence = str(record.seq)
		gaps = re.findall(r'(-+)', sequence)
		gaps_lengths.extend([len(gap) for gap in gaps])

	return len(gaps_lengths)

def get_min_max_gap_length(msa):

	if isinstance(msa, str):
		msa = get_msa_from_file(msa)

	gaps_lengths = []
	for record in msa:
		sequence = str(record.seq)
		gaps = re.findall(r'(-+)', sequence)
		gaps_lengths.extend([len(gap) for gap in gaps])

	if not gaps_lengths:
		return None

	return (np.min(gaps_lengths), np.max(gaps_lengths))


def get_average_length_sequences(msa):
	if isinstance(msa, str):
		msa = get_msa_from_file(msa)
	seq_lengths = [len(record.seq.ungap("-")) for record in msa]
	return np.average(seq_lengths)

def remove_masked_sites(msa, dest_filename=None):
	"""
	:param msa: bio.AlignIO format or path to msa file
	:return:
	"""
	if isinstance(msa, str):
		msa = get_msa_from_file(msa)
	ntaxa = len(msa)
	nchars = msa.get_alignment_length()
	new_msa = copy.deepcopy(msa)
	for col_i in range(nchars - 1, -1, -1):
		col = msa[:, col_i]
		print(col)
		if not re.search("[ACGTacgt]", col, re.IGNORECASE):
			new_msa = new_msa[:, :col_i] + new_msa[:, col_i + 1:]
	if dest_filename:
		with open(dest_filename, "w") as fpw:
			AlignIO.write(new_msa, fpw, format=PHYLIP_FORMAT)
	return new_msa


def remove_gapped_sites(msa, thres):
	"""
	removes sites that contain more than thres gaps in a column
	:param msa: a Bio.Align.MultipleSeqAlignment object
	:param thres: a floating number in [0,1], the maximal fraction of
	sites that may hold gaps within every alignment column
	:return: a new msa without sites that have more than thres gaps
	"""
	ntaxa = len(msa)
	nchars = msa.get_alignment_length()
	new_msa = copy.deepcopy(msa)
	for col_i in range(nchars - 1, -1, -1):
		if msa[:, col_i].count("-") / ntaxa > thres:
			new_msa = new_msa[:, :col_i] + new_msa[:, col_i + 1:]
	return new_msa

'''
def convert_phylip_to_nexus(input_file, output_file):
	AlignIO.convert(input_file, PHYLIP_FORMAT, output_file, NEXUS_FORMAT, alphabet=Alphabet.generic_dna)
'''

def convert_fas_to_phylip(input_file, output_file):
	AlignIO.convert(input_file, FASTA_FORMAT, output_file, PHYLIP_FORMAT)


def convert_sequences_ids(msa, output="new_msa.phy"):
	"""
		:param msa: bio.AlignIO format or path to msa file
		:return: msa with sequential names of the sequences S0001, S0002...
	"""
	if isinstance(msa, str):
		msa = get_msa_from_file(msa)

	for i, record in zip(range(1,len(msa)+1),msa):
		record.id = str(i).zfill(4)

	with open(output, "w") as output_handle:
		AlignIO.write(msa, output_handle, PHYLIP_FORMAT)

def convert_phylipInterleaved_to_sequential_relaxed(msa_file, output_file):
	with open(msa_file, "rU") as input_handle:
		alignments = AlignIO.read(input_handle, PHYLIP_FORMAT)

	with open(output_file, "w") as output_handle:
		out_handle = AlignIO.PhylipIO.SequentialPhylipWriter(output_handle)
		out_handle.write_alignment(alignments, id_width=30)


if __name__ == '__main__':

	#print(remove_masked_sites("real_msa.phy"))
	convert_sequences_ids("EMGT00050000000001.Drosophila.001.aa.fas", output="new_msa.phy")