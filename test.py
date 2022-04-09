import numpy as np

a = np.array([[[1],[2],[3]],[[1],[2],[3]]])
b = np.array([[[4],[5],[6]]])

# a[0] = [2,3]
print(a.shape)
c = np.zeros((2,3,2))
for i in range(b.shape[0]):
    for j in range(3):
        c[i,j] = np.append(a[i,j],b[i,j])
for i in range(b.shape[0],a.shape[0]):
    for j in range(3):
        c[i,j,:1] = a[i,j]
print(c)

