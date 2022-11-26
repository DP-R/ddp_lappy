import numpy as np



def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
        print('yes\t',end='')
        return v
    return v/norm

def g(x):
    return np.max(x, 0)   # Keep compatiable with numpy in 1.14.0 version


def distance_agent_to_wall(point, wall):
    p0 = np.array([wall[0],wall[1]])
    p1 = np.array([wall[2],wall[3]])
    d = p1-p0
    ymp0 = point-p0
    t = np.dot(d,ymp0)/np.dot(d,d)
    if t <= 0.0:
        dist = np.sqrt(np.dot(ymp0,ymp0))
        cross = p0 + t*d
    elif t >= 1.0:
        ymp1 = point-p1
        dist = np.sqrt(np.dot(ymp1,ymp1))
        cross = p0 + t*d
    else:
        cross = p0 + t*d
        dist = np.linalg.norm(cross-point)
    npw = normalize(cross-point)
    # print(dist,'\t',npw,)
    # print(d,ymp0,t)
    return dist,npw

# print(np.linalg.norm(np.array([1,10])-np.array([9,99])))
# print(normalize([1,1]))
