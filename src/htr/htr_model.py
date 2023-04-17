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
        pass

    def setup_rnn(self) -> None:
        pass

    def setup_ctc(self) -> None:
        pass

    def setup_tf(self) -> Tuple[tf.compat.v1.Session, tf.compat.v1.train.Saver]:
        pass
