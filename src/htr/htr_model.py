# htr model
from typing import List, Tuple
import tensorflow as tf


class DecoderType:
    """ CTC decoder types """
    BestPath = 0
    BeamSearch = 1
    WordBeamSearch = 2


class Model:
    """ Tensorflow model for HTR """
    def __init__(self, chars: List[str], decoder: str = DecoderType.BestPath,
                 restore: bool = False, dump: bool = False) -> None:
        self.dump = dump
        self.chars = chars
        self.decoder = decoder
        self.restore = restore
        self.snap_ID = 0

        # normalise over a batch or population
        # tf placeholder for data assigned later - datatype: boolean, name: is_train
        # tf.compat.v1 allows use of the depreciated placeholder in tf v2
        self.is_train = tf.compat.v1.placeholder(tf.bool, name='is_train')

        # input image batch
        self.input_imgs = tf.compat.v1.placeholder(tf.float32, shape=(None, None, None))

        # setup CNN, RNN and CTC layers for NN
        self.setup_cnn()
        self.setup_rnn()
        self.setup_ctc()

        # setup optimizer to train Neural Network
        self.batches_trained = 0
        self.update_ops = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.UPDATE_OPS)
        with tf.control_dependencies(self.update_ops):
            self.optimiser = tf.compat.v1.train.AdamOptimizer().minimize(self.loss)

        self.session, self.saver = self.setup_tf  # initialize tf

    def setup_cnn(self) -> None:
        """ Creates Convolution Neural Network (CNN) Layers (currently NN consists of 5 CNN layers) """

        # convert input img to 4D by adding a dimension (tensor) at axis 3
        cnn_4d = tf.expand_dims(input=self.input_imgs, axis=3)

        # list of parameters for the layers
        kernel_vals = [5, 5, 3, 3, 3]  # 5x5 kernel for first 2 layers, 3x3 for final 3 layers
        feature_vals = [1, 32, 64, 128, 128, 256]
        stride_vals = pool_vals = [(2, 2), (2, 2), (1, 2), (1, 2), (1, 2)]
        num_layers = len(stride_vals)  # currently 5 CNN layers

        # create layers
        pool = cnn_4d  # input into first CNN layer
        for i in range(num_layers):  # loop over all CNN layers - extract relevant features

            # variable Tensor - 4D for 2D convolution operation
            kernel = tf.Variable(
                tf.random.truncated_normal([kernel_vals[i], kernel_vals[i], feature_vals[i],
                                            feature_vals[i + 1]], stddev=0.1))

            # 2D convolution using same padding -> set stride of sliding window to 1
            convolution = tf.nn.conv2d(input=pool, filters=kernel, padding='SAME', strides=(1, 1, 1, 1))
            norm_conv = tf.compat.v1.layers.batch_normalization(convolution, training=self.is_train)  # normalised conv

            # RELU activation function
            relu = tf.nn.relu(norm_conv)  # non-linear RELU - returns 0 for negative vals, returns val if positive

            # summarises image regions outputting downsized (pooled) versions of the input
            pool = tf.nn.max_pool2d(input=relu, ksize=(1, pool_vals[i][0], pool_vals[i][1], 1),
                                    strides=(1, stride_vals[i][0], stride_vals[i][1], 1), padding='VALID')

        self.cnn_4d_out = pool

    def setup_rnn(self) -> None:
        pass

    def setup_ctc(self) -> None:
        pass

    def setup_tf(self) -> Tuple[tf.compat.v1.Session, tf.compat.v1.train.Saver]:
        pass
