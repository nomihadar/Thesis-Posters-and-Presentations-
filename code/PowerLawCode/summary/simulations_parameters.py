import sys, os

__author__ = 'Nomi'

sys.path.append(os.path.dirname(sys.path[0]))

from defs import *

def simulations_parameters(dic, output_name):

    frames = []
    for id, rel_path in dic.items():
        indel_file = os.path.join(DATA_PATH, rel_path, SIMULATIONS_DIR,
                                  INDEL_MODEL_OUTPUT)
        df = pd.read_csv(indel_file,)
        df[ID_COL] = id
        frames.append(df)

    df2 = pd.concat(frames)
    df2.set_index(ID_COL, inplace=True)
    df2.to_csv(output_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', required=False,
                        help='file of paths')
    parser.add_argument('-o', required=True,
                        help='output name')
    args = parser.parse_args()

    if args.f:
        df = pd.read_csv(args.f)
        dic = df.set_index(ID_COL)[PATH_COL].to_dict()
    else:
        dic = DIC

    simulations_parameters(dic, args.o)



