import pickle


def save_r_new_vector(obj, range):
    with open('r_new_vector/' + range + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_r_new_vector(range):
    with open('r_new_vector/' + range + '.pkl', 'rb') as f:
        return pickle.load(f)


# M_vector按照fromNodeId范围来存，第一批就是range=1000
def save_M_vector(obj, range):
    with open('m_vector/' + range + '.pkl', "ab+") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_M_vector(range):
    dict_m_slice = {}
    with open('m_vector/' + range + '.pkl', 'rb') as f:
        while True:
            try:
                m = pickle.load(f)
                for key in m.keys():
                    dict_m_slice[key] = m[key]
            except EOFError:
                break
    return dict_m_slice


# r_vector按照递归次数来存，例如初始值就是recur=0

def save_r_vector(obj, recur):
    with open('r_vector/' + recur + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_r_vector(recur):
    with open('r_vector/' + recur + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_deadEnd_list(obj, name):
    with open('deadEndList/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_deadEnd_list(name):
    with open('deadEndList/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
