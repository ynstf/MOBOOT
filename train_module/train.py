import tflearn
import tensorflow as tf

tf.reset_default_graph()

def neural_net(training,output):
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 10)
    net = tflearn.fully_connected(net, 10)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation = "softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    return model