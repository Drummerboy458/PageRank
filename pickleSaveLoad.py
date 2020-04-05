import pickle

#M_vector按照fromNodeId范围来存，第一批就是range=1000
def save_M_vector(obj, range ):
    with open('m_vector/'+ range + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_M_vector(range):
    with open('m_vector/' + range + '.pkl', 'rb') as f:
        return pickle.load(f)

#r_vector按照递归次数来存，例如初始值就是recur=0

def save_r_vector(obj, recur ):
    with open('r_vector/'+ recur + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_r_vector(recur):
    with open('r_vector/' + recur + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_deadEnd_list(obj, name ):
    with open('deadEndList/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_deadEnd_list(name):
    with open('deadEndList/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
