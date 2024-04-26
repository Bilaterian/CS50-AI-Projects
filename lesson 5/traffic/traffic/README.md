The initial version of the model was copied from given code from src5. This led me to the first setup of the convolutional neural network:
- 1 32 layer conv2D filter using a 3x3 sampling layer
- 1 Max Pooling layer using a 2x2 pool
- 1 flattening layer
- 1 hidden layer using 128 nodes
- 1 dropout layer with a 0.5 chance of dropping
- 1 output layer using num categories of nodes
Initial results fell into accuracy: 0.0560 - loss: 3.5020.

The first thing I tried was adding another Conv2D layer after the max pooling, this time with a sample size of 4x4.I also increased the hidden layer to using 128 nodes to match the number of nodes after the second Conv2D.
The results after the changes were: accuracy: 0.9340 - loss: 0.2703, which was an immediate improvement.

I tried adding additional hidden layers to help with accuracy but this only backfired, leading to score similar to the initial results. The next thing I tried was switching ReLU with a leaky ReLU for the hidden layer, which showed negligible improvements. The results after adding leaky ReLU were accuracy: 0.9380 - loss: 0.2584.

Finally, I adjusted the  dropout layer to a 0.3 chance of dropping. Given that the sample street signs are all polygons, I thought that a 0.5 dropout rate was too aggressive, since octagonal stop signs looked similar to circles in shape. this led to a final result of accuracy: 0.9475 - loss: 0.2603, which  again is negligible in improvement.