# htr model
from typing import List, Tuple
import tensorflow as tf
import sys
from htr_loaddata import Batch
import numpy as np


class DecoderType:
    """ CTC decoder types """
    BestPath = 0
    BeamSearch = 1
    WordBeamSearch = 2


class Model:
    """ Tensorflow model for HTR """

    def __init__(self, chars: List[str], decoder_type: str = DecoderType.BestPath,
                 restore: bool = False, dump: bool = False) -> None:
        self.dump = dump
        self.chars = chars
        self.decoder_type = decoder_type
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
            # create a kernel of kernal_vals[i] x kernal_vals[i]
            kernel = tf.Variable(
                tf.random.truncated_normal([kernel_vals[i], kernel_vals[i], feature_vals[i],
                                            feature_vals[i + 1]], stddev=0.1))

            # 2D convolution using same padding + kernel -> set stride of sliding window to 1
            convolution = tf.nn.conv2d(input=pool, filters=kernel, padding='SAME', strides=(1, 1, 1, 1))
            norm_conv = tf.compat.v1.layers.batch_normalization(convolution, training=self.is_train)  # normalised conv

            # RELU activation function -> takes normalised convolution as input
            relu = tf.nn.relu(norm_conv)  # non-linear RELU - returns 0 for negative vals, returns val if positive

            # summarises image regions outputting downsized (pooled) versions of the input
            # size pool_val x pool_val | step-size stride_val x stride_val
            pool = tf.nn.max_pool2d(input=relu, ksize=(1, pool_vals[i][0], pool_vals[i][1], 1),
                                    strides=(1, stride_vals[i][0], stride_vals[i][1], 1), padding='VALID')

        self.cnn_4d_out = pool

    def setup_rnn(self) -> None:
        """ Create LSTM Recurrent Neural Network (RNN) Layers (2 RNN layers) """

        #  feed output of CNN into RNN layers
        rnn_3d = tf.squeeze(self.cnn_4d_out, axis=[2])  # remove dimensions of size 2 from tensor

        features = 256  # 256 features fed into each timestep (taken from output of CNN)

        # basic LSTM cells use in building RNN -> 2 RNN layers
        # state_is_tuple returns 2-tuples of c_state (cell) and m_state (hidden/memory)
        cells = [tf.compat.v1.nn.rnn_cell.LSTMCell(num_units=features, state_is_tuple=True) for layer in range(2)]
        stacked = tf.compat.v1.nn.rnn_cell.MultiRNNCell(cells, state_is_tuple=True)  # stack multiple LSTM basic cells

        # Bidirectional RNN - forward + backwards (2 output seqs 32x256)
        (fw, bw), _ = tf.compat.v1.nn.bidirectional_dynamic_rnn(cell_fw=stacked, cell_bw=stacked,
                                                                input=rnn_3d, dtype=rnn_3d.dtype)

        # concatenate forward + backwards cells along the 2nd dimension -> expand dimension @ axis 2
        concat = tf.expand_dims(tf.concat([fw, bw], 2), 2)  # outputs seq of size 32x512

        # project output to chars (including blank for ctc) = 80 chars
        kernel = tf.Variable(tf.random.truncated_normal([1, 1, features * 2, len(self.chars) + 1], stddev=0.1))
        self.rnn_out_3d = tf.squeeze(tf.nn.atrous_conv2d(value=concat, filters=kernel, rate=1, padding='SAME'),
                                     axis=[2])  # computes 2D atrous convolution (dilated conv) on 4D concat
        # dilation rate = 1 => no gaps (tale every 1st element)

    def setup_ctc(self) -> None:
        """ Connectionist Temporal Classification (CTC) loss and decoder """
        self.ctc_3d = tf.transpose(a=self.rnn_out_3d, perm=[1, 0, 2])  # tranposed matrix from RNN

        # ground truth texts encoded as sparse tensor -> 3 separate dense tensors (indices, values, dense_shape)
        self.gt = tf.SparseTensor(tf.compat.v1.placeholder(tf.int64, shape=[None, 2]),
                                  tf.compat.v1.placeholder(tf.int32, [None]),
                                  tf.compat.v1.placeholder(tf.int64, [2]))

        self.seq_len = tf.compat.v1.placeholder(tf.int32, [None])  # input seq len (passed into CTC loss and decoding)

        # calculate loss for batch -> find mean of elements across dimensions of ctc loss tensor
        self.loss = tf.reduce_mean(
            input_tensor=tf.compat.v1.nn.ctc_loss(labels=self.gt, inputs=self.ctc_3d,
                                                  sequence_length=self.seq_len,
                                                  ctc_merge_repeated=True))

        # ctc loss for each element to compute label probability
        self.saved_ctc_input = tf.compat.v1.placeholder(tf.float32, shape=[None, None, len(self.chars) + 1])
        self.loss_per_element = tf.compat.v1.nn.ctc_loss(labels=self.gt, inputs=self.saved_ctc_input,
                                                         sequence_length=self.seq_len, ctc_merge_repeated=True)

        # CTC Decoders
        # Decode using Best Path
        if self.decoder_type == DecoderType.BestPath:
            self.decoder = tf.nn.ctc_greedy_decoder(inputs=self.ctc_3d, sequence_length=self.seq_len)

        # Decode using Beam Search
        elif self.decoder_type == DecoderType.BeamSearch:
            self.decoder = tf.nn.ctc_beam_search_decoder(inputs=self.ctc_3d, sequence_length=self.seq_len,
                                                         beam_width=50)

    def setup_tf(self) -> Tuple[tf.compat.v1.Session, tf.compat.v1.train.Saver]:
        """ Setup Tensorflow """
        # print tf and python versions
        print('Python: ' + sys.version)
        print('Tensorflow: ' + tf.__version__)

        session = tf.compat.v1.Session()  # open tf session
        saver = tf.compat.v1.train.Saver(max_to_keep=1)  # keeps max 1 checkpoint file
        model_dir = './model/'
        snapshot = tf.train.latest_checkpoint(model_dir)  # retrieves checkpoint state from the model dir

        # to restore model for inference requires an existing latest snapshot
        if self.restore and not snapshot:
            raise Exception('No saved model found in: ' + model_dir)

        # loading model if available
        if snapshot:
            print('Initiating with stored values from ' + snapshot)
            saver.restore(session, snapshot)
        else:
            print('Initiating with new values...')
            session.run(tf.compat.v1.global_variables_initializer())

        return session, saver

    def to_sparse(self, texts: List[str]) -> Tuple[List[List[int]], List[int], List[int]]:
        """ Convert ground texts into sparse tensors """

        # 3 component dense tensors of the sparse tensor
        indices, vals = [], []
        shape = [len(texts), 0]  # last entry = max(labelList[i])

        # loop over all ground texts
        for ele, text in enumerate(texts):

            # convert to label string (class-id)
            labels = [self.chars.index(c) for c in text]

            # check that sparse tensor has size of max label
            if len(labels) > shape[1]:
                shape[1] = len(labels)

            # convert each label into sparse tensor i.e. populate the dense tensors: indices and values
            for i, label in enumerate(labels):
                indices.append([ele, i])
                vals.append(label)

        return indices, vals, shape

    def train_batch(self, batch: Batch) -> float:
        """ Train NN using batch """
        num_batches = len(batch.imgs)
        max_len = batch.imgs[0].shape[0] // 4
        sparse = self.to_sparse(batch.gt_texts)  # convert gts to sparse tensors

        eval = [self.optimiser, self.loss]

        # feeds values to tf placeholders
        feed_dict = {
            self.input_imgs: batch.imgs,
            self.gt: sparse,
            self.seq_len: [max_len] * num_batches,
            self.is_train: True
        }

        _, loss = self.session.run(eval, feed_dict)  # run tf session
        self.batches_trained += 1  # increment trained batches count

        return loss

    def to_text(self, ctc_output: tuple, batchsize: int) -> List[str]:  #
        """ Extract texts from CTC decoder output """

        # TF Decoders: label strings in sparse tensor
        decoded = ctc_output[0][0]  # first element (sparse tensor) of ctc output
        labels_str = [[] for _ in range(batchsize)]  # list of label strings for each batch element

        # loop over all indices
        for (index, index_2d) in enumerate(decoded.indices):
            label = decoded.vals[index]
            batch_ele = index_2d[0]
            labels_str[batch_ele].append(label)

        # map labels to chars for all batch elements
        return [''.join([self.chars[c] for c in labelStr]) for labelStr in labels_str]

    def inference_batch(self, batch: Batch, calc_prob: bool = False, gt_prob: bool = False):
        """ Recognise texts in a batch using the NN """

        num_batches = len(batch.imgs)
        eval = []  # tensors to be evaluated

        if calc_prob:
            eval.append(self.ctc_3d)

        # seq length depends on size of input image
        max_len = batch.imgs[0].shape[0] // 4

        # feed tensors into model
        feed_dict = {
            self.input_imgs: batch.imgs,
            self.seq_len: [max_len] * num_batches,
            self.is_train: True
        }

        eval_result = self.session.run(eval, feed_dict)  # evaluation

        decoded = eval_result[0]  # tf decoders perform decoding in TF graph

        # map labels to char string
        texts = self.to_text(decoded, num_batches)

        # feed RNN and recognised text into CTC loss to calc labeling prob
        prob = None
        if calc_prob:
            sparse = self.to_sparse(batch.gt_texts) if gt_prob else self.to_sparse(texts)
            ctc_input = eval_result[1]  # feed into ctc
            eval_lst = self.loss_per_element
            feed_dict = {
                self.saved_ctc_input: ctc_input,
                self.gt: sparse,
                self.seq_len: [max_len] * num_batches,
                self.is_train: False
            }

            loss = self.session.run(eval_lst, feed_dict)
            prob = np.exp(-loss)

        return texts, prob
