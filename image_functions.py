import numpy as np
from skimage.measure import shannon_entropy
from PIL import Image, ImageTk

class Node:
    def __init__(self, img):
        self.img = img
        self.entropy = shannon_entropy(img)
        
    def get_entropy(self):
        return self.entropy
    
    def get_image(self):
        return self.img


# Array to TKImage
def arr2im(image, dims):
    imagePIL = Image.fromarray(image)
    imagePIL.thumbnail(dims, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image=imagePIL)


# Splits Parent Matrix into 4 Children Matrices
def split(parent):
    mat = parent.get_image()
    m, n, l = mat.shape

    A_mat = mat[0:int(m/2), 0:int(n/2), :]
    B_mat = mat[0:int(m/2), int(n/2):n, :]
    C_mat = mat[int(m/2):m, 0:int(n/2), :]
    D_mat = mat[int(m/2):m, int(n/2):n, :]

    A = Node(A_mat)
    B = Node(B_mat)
    C = Node(C_mat)
    D = Node(D_mat)
    
    splits = A, B, C, D
    
    return np.asarray(splits, dtype = object)


# Returns Array of Entropy of Corresponding Partitions
def get_entropy(mats):
    n = len(mats)
    entropy = np.zeros(n)
    for ii in range(n):
        entropy[ii] = mats[ii].get_entropy()
    return entropy

# Partitions All Nodes Whose Entropy is Above the Given Threshold
def deconstructor(parent, ent_thresh):
    global split_iter
    child = np.empty(0, dtype='object')
    ent = get_entropy(parent)
    for ii in range(len(parent)):
        if (ent[ii] > ent_thresh):
            child = np.append(child, split(parent[ii]))
        else:
            child = np.append(child, parent[ii])
    parent = child

    return parent

# Draws Border Around 
def draw_border(children):
    n = len(children)
    for j in range(n):
        cur_img = np.copy(children[j].get_image())

        cur_img[0:-1,    0, :] = 255
        cur_img[0:-1,   -1, :] = 255
        cur_img[0   , 0:-1, :] = 255
        cur_img[-1  , 0:-1, :] = 255
        
        children[j] = Node(cur_img)

    return children

def combine(parent, i):
    top = np.vstack((parent[i].get_image(), parent[i+2].get_image()))
    bot = np.vstack((parent[i+1].get_image(), parent[i+3].get_image()))
    img = np.hstack((top, bot))

    return Node(img)

def reconstructor(parents, viz_flag = 0):
    children = np.copy(parents)
    if viz_flag == 0:
        draw_border(children)
    n = len(children)
    num = 0
    while n != 1:
        print("Iter:", num)
        num += 1
        p1 = 0
        p1_image = children[0].get_image()
        p1_shape = p1_image.shape[1]

        for ii in range(n):
            p2 = ii
            
            p2_image = children[p2].get_image()
            p2_shape = p2_image.shape[1]


            if abs(p1_shape - p2_shape) > 1:
                p1 = p2
                p1_image = children[p1].get_image()
                p1_shape = p1_image.shape[1]

            if (p2-p1 == 3):
                children[p1] = combine(children, p1)
                children = np.delete(children, [p1+1, p1+2, p1+3])
                n = len(children)
                break

    return children[0].get_image()
