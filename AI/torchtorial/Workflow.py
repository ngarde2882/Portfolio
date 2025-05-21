import torch
from torch import nn
import matplotlib.pyplot as plt
device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.set_default_device(device)
print(f'default device set to: {device}')


### WORKFLOW ###
# 1. get data readyd
# 2. build model / pretrained model
#     2.1 loss function & optimizer
#     2.2 training loop
# 3. fit model to data
#     3.1 make predictions
# 4. evaluate models
# 5. improve through experimentation
# 6. save / reload model

### DATA ###
# 1. get data into numerical representation
# 2. build a model to learn patterns in that representation
weight = 0.7
bias = 0.3

x = torch.arange(0,1.02,0.02).unsqueeze(1)
y = weight*x + bias

# separate data into training and test datasets
# training -> validation -> test set            amt data    how often used
# training    model learns from this data         60-80%      Always
# validation  model gets tuned on this data       10-20%      Often
# testing     model gets evaluated on this data   10-20%      Always
train_split = int(0.8 * len(x))
xtrain, ytrain = x[:train_split], y[:train_split]
xtest, ytest = x[train_split:], y[train_split:]

def plot_predictions(train_data=xtrain,
                     train_label=ytrain,
                     test_data=xtest,
                     test_label=ytest,
                     predictions=None):
    # plots training data and compares predictions
    plt.figure(figsize=(10,7))
    plt.scatter(train_data,train_label,c='b',s=4,label='Training Data')
    plt.scatter(test_data,test_label,c='cyan',s=4,label='Testing Data')
    if predictions != None:
        plt.scatter(test_data,predictions,c='r',s=4,label='Predictions')
    plt.legend(prop={'size':14})
    plt.show()

class LinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__() # inherit nn.Module init
        self.weights = nn.Parameter(torch.randn(1,requires_grad=True,dtype=torch.float)) # simple data set means we can decide our parameters
        self.bias = nn.Parameter(torch.randn(1,requires_grad=True,dtype=torch.float)) # nn.Module can set these itself
    def forward(self, x:torch.Tensor)->torch.Tensor: # defines computation performed at every call
        return self.weights*x+self.bias

# plot_predictions(xtrain,ytrain,xtest,ytest)
plot_predictions(predictions=None)

### MODEL BUILDING ESSENTIALS ###
# torch.nn contains all the buildings for commputational graphs
# torch.nn.Parameter what parameters should our model try and learn
    # often a pytorch layer from torch.nn will set these for us
# torch.nn.Model base class for nn modules
    # when you subclass nn.Module, overwrite the forward(self, in) function
# torch.optim optimizers that aid with gradient descent and reduce loss
# torch.utils.data.Dataset and .Dataloader for data representation an loading

model0 = LinearRegressionModel()
print(list(model0.parameters()))
print(model0.state_dict())

# predict ytest based on xtestusing forward()
with torch.inference_mode(): # speeds up predictions
    ypredict = model0(xtest)

print(ypredict)
plot_predictions(predictions=ypredict)

# use a loss function to measure accuracy
    # nn.L1Loss  mean absolute error  |predicted-target|
    # nn.MSELoss mean squared error   (predicted-target)^2
    # nn.BCELoss binary cross entropy loss, good for classification problems like photo->cat?dog?
# use an optimizer, takes into account the loss f(x) and adjusts model parameters
# torch.optim
    # .SGD sochastic gradient descent (random derivatives to minimize loss fn)
# in PyTorch we need a:
#     training loop
#     testing loop

### LOSS FUNCTION ###
lossfn = nn.L1Loss()
### OPTIMIZER ###
optimizer = torch.optim.SGD(params=model0.parameters(), # parameters that need to be optimized
                            lr=0.01) # learning rate, how big a step when adjusting parameters
### TRAINING LOOP ###
# 0. loop through data
# 1. forward pass to make predictions
# 2. calc loss and compare predictions to ground truth labels
# 3. optimizer zero grad
# 4. loss backprop to calc gradients with respect to loss
# 5. optimizer grad-descent adjusts params to attempt to decrease loss
epochs = 1 # each epoch is a loop through the data
for epoch in range(epochs): # 0. loop through data
    model0.train() # set to training mode, turns on gradient tracking
    # 1. forward pass
    ypredict = model0(xtrain) # this calls forward
    # 2. calc loss
    loss = lossfn(ypredict,ytrain) # input, target
    # 3. optimizer zero grad
    optimizer.zero_grad() # reset optimizer changes
    # 4. loss backprop
    loss.backward()
    # 5. step optimizer
    optimizer.step() # optimizer changes accumulate, zero them in step 3. for next iteration
    model0.eval() # set to testing mode, turns off gradient tracking
