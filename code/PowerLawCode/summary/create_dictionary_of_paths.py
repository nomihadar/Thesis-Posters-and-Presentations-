import sys, os

__author__ = 'Nomi'

sys.path.append(os.path.dirname(sys.path[0]))

from defs import *

TITLES = ['id', 'path', 'db']

def msa_features(root_path, output_name):

    data = {name: [] for name in TITLES}
    exceptions = []

    id = 1
    for root, dirs, files in os.walk(root_path, topdown=True):
        for file in files:
            if file.endswith(REF_MSA_PHY):

                rel_dir = os.path.relpath(root, root_path)

                db = ""
                for db in DATA_BASES:
                    if db in root:
                        db = db
                        break

                data[TITLES[0]].append(id)
                data[TITLES[1]].append(rel_dir)
                data[TITLES[2]].append(db)

                id += 1

    df = pd.DataFrame(data)
    df = df[TITLES]
    df.to_csv(output_name, index=False)

    d = {"exceptions": exceptions}
    df = pd.DataFrame(d)
    df.to_csv("exceptions.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-root', required=False,
                        help='root path', default=DATA_PATH)
    parser.add_argument('-o', required=True,
                        help='output name')
    args = parser.parse_args()

    msa_features(args.root, args.o)


