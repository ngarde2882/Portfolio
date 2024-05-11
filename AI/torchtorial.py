import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
### TEST ###
# print(torch.__version__)
# x = torch.rand(5, 3)
# print(x)

### TENSORS ###
x = torch.tensor([[1,2,3],[4,5,6],[7,8,9]])
# print(x)
# print(x.pow(2))
# print(x.pow(2).sum())
# 
# x = torch.tensor([[1., -1.], [1., 1.]], requires_grad=True)
# out = x.pow(2).sum()
# out.backward()
#
scalar = torch.tensor(7)
vector = torch.tensor([7,7])
MATRIX = torch.tensor([[7,8],[9,10]])
TENSOR = torch.tensor([[[1,2,3],
                        [3,6,9],
                        [2,4,5]]])
big_tensor = torch.tensor([[[[2,2],[3,3]],
                            [[4,4],[5,5]],
                            [[6,6],[7,7]],],
                           [[[0,0],[1,1]],
                            [[9,9],[8,8]],
                            [[1,0],[0,1]]]])
# s.ndim = v.ndim = 1, M.ndim = 2, T.ndim = 3, bt.ndim = 4
# s.shape = torch.Size(1), v.shape = torch.Size(2), M.shape = torch.Size([2,2]), T.shape = torch.Size([1,3,3]), bt.shape = torch.Size([2,3,2,2])
### RANDOM TENSORS ###
# NNs typically init random and adjust with data
random_tensor = torch.rand(2,3,2,2)
random_normaldist_tensor = torch.randn(2,3,2,2)
random_image_tensor = torch.rand(256,256,3) # H X W X color channels (R,G,B)
### FUNCTIONS ###
zeros = torch.zeros(2,3,2,2) # fills tensor with 0s
zeros = torch.zeros_like(big_tensor) # zeros_like gets the shape of the input and makes a tensor of that shape filled with 0s
ones = torch.ones(2,3,2,2) # fills tensor with 1s
ones = torch.ones_like(big_tensor) # read 2 lines up
arranged = torch.arange(0,10) # creates a 1d torch.Size([10]) : [0,1,2,..,8,9]
arranged = torch.arange(start=0,end=77,step=7) # start (inclusive), end (exclusive), step : [0,7,14,..,63,70]
### TENSOR PARAMETERS ###
x = torch.tensor([3,1,4,1,5,9,2],
                dtype=None, # tensor datatype (e.g. float16,64, int8,128, bool)    default : float32
                device=None, # where the tensor is located ('cpu','gpu')           default : 'cpu'
                requires_grad=False) # track gradient on tensor                    default : False (don't track)
### TENSOR MANIPULATION ###
# addition, subtraction, elem-wise multiplication, division, matrix multiplication
# scalar
xp100 = x + 100
xm1 = x - 1
xt5 = x * 5
xd2 = x / 2
# matrix mult
torch.matmul(torch.tensor([[2,3],[4,5],[6,7]]),torch.tensor([[8,9,10],[11,12,13]])) # dot product : tensor([[49,54,59],[87,96,105],[125,138,151]])
torch.tensor([[2,3],[4,5],[6,7]]) @ torch.tensor([[8,9,10],[11,12,13]]) # same thing ^
torch.rand(4,5) @ torch.rand(5,6) # inner dimensions must match (5,5), returns shape of outer dimensions (4,6)
x.T # transpose matrix
x.min(),x.max(),x.mean() # stats functions
# reshaping, view, stack (combine), squeeze (remove 1 dimenstion), unsqueeze (add 1 dimension), permute
# reshape
x = torch.arange(1,10) # [1,2,..,8,9] list of 9
xr = x.reshape(9,1) # [[1],[2],..,[8],[9]] 9 lists of 1 (vertical)
xr = x.reshape(3,3) # [[1,2,3],[4,5,6],[7,8,9]] 3 lists of 3
# view (views share the same memory as the tensor the are made from)
v = x.view(3,3) # v is now the same values as x reshaped into 3,3
x[0]=-1 # x[0] = -1, v[0] = [-1,2,3]
v[0]=-1 # x[0:3] = -1, v[0] = [-1,-1,-1]
# stack (you can only stack tensors of the same shape)
s = torch.stack([x,x,x]) # shaped [3,9], apends the tensors together [x],[x],[x]
s = torch.stack([x,x,x], dim=1) # shaped [9,3], apends the tensors together by index [[x[0],x[0],x[0]],..,[x[8],x[8],x[8]]]
# squeeze
x = torch.arange(1,10) # shape is [9]
xr = x.reshape(1,9) # shape is [1,9]
sq = xr.squeeze() # squeeze trims dim=1, shape is [9]
sq.unsqueeze() # adds the dimension back [1,9]
sq.unsqueeze(dim=1) # makes the shape [9,1]
# permute (rearrange dimensions and share memory like view)
# torch.permute(tensor, (dimension indecies)) : x.shape=[2,3,5], torch.permute(x,(2,0,1)).shape=[5,2,3]
# use x.permute(indecies)
random_image_tensor = torch.rand(256,256,3) # H,W,color channels
p = random_image_tensor.permute(2,0,1) # cc,H,W
### NUMPY TO TENSOR ###
# torch.from_numpy(arry) numpy default type is float64, pytorch default is float32
### REPEATABILITY ###
# NNs start with random numbers, perform tensor operations, update random numbers, repeat
seed = 42
a = torch.rand(3,4)
b = torch.rand(3,4)
# most likeley all false
seed = 42
a = torch.rand(3,4)
seed = 42
b = torch.rand(3,4)
# all true
### GPUs ###

