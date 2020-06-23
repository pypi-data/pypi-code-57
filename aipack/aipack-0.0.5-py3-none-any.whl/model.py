import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Input, Conv2D, ReLU, LeakyReLU
from .anchor import decode_tf, prior_box_tf


class BatchNormalization(tf.keras.layers.BatchNormalization):
    """Make trainable=False freze BN for real (the og version is sad).
       ref: https://github.com/zzh8829/yolov3-tf2
    """
    def __init__(self, axis=-1, momentum=0.9, epsilon=1e-5, center=True,
                 scale=True, name=None, **kwargs):
        super(BatchNormalization, self).__init__(
            axis=axis, momentum=momentum, epsilon=epsilon, center=center,
            scale=scale, name=name, **kwargs)

    def call(self, x, training=False):
        if training is None:
            training = tf.constant(False)
        training = tf.logical_and(training, self.trainable)

        return super().call(x, training)


class ConvUnit(tf.keras.layers.Layer):
    """Conv + BN + Act"""
    def __init__(self, filters, kernel_size, strides, weight_decay, activation=None, name='ConvBN', **kwargs):
        super(ConvUnit, self).__init__(name=name, **kwargs)
        self.conv = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding='same',
                           kernel_initializer=tf.keras.initializers.he_normal(),
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay),
                           use_bias=False, name='conv')
        self.bn = BatchNormalization(name='bn')

        if activation is None:
            self.activation_fn = tf.identity
        elif activation == 'relu':
            self.activation_fn = ReLU()
        elif activation == 'lrelu':
            self.activation_fn = LeakyReLU(0.1)
        else:
            raise NotImplementedError(
                'Activation function type {} is not recognized.'.format(activation))

    def call(self, x):
        return self.activation_fn(self.bn(self.conv(x)))


class FPN(tf.keras.layers.Layer):
    """Feature Pyramid Network"""
    def __init__(self, out_channel, weight_decay, name='FPN', **kwargs):
        super(FPN, self).__init__(name=name, **kwargs)
        activation = 'relu'

        # 깊은 신경망의 경우 lrelu를 통해 학습이 0으로 수렴하는 오류를 방지합니다.
        if (out_channel <= 64):
            activation = 'lrelu'

        self.output1 = ConvUnit(filters=out_channel, kernel_size=1, strides=1, weight_decay=weight_decay, activation=activation)
        self.output2 = ConvUnit(filters=out_channel, kernel_size=1, strides=1, weight_decay=weight_decay, activation=activation)
        self.output3 = ConvUnit(filters=out_channel, kernel_size=1, strides=1, weight_decay=weight_decay, activation=activation)
        self.merge1 = ConvUnit(filters=out_channel, kernel_size=3, strides=1, weight_decay=weight_decay, activation=activation)
        self.merge2 = ConvUnit(filters=out_channel, kernel_size=3, strides=1, weight_decay=weight_decay, activation=activation)

    def call(self, x):
        output1 = self.output1(x[0])  # [80, 80, out_channel]
        output2 = self.output2(x[1])  # [40, 40, out_channel]
        output3 = self.output3(x[2])  # [20, 20, out_channel]

        up_h, up_w = tf.shape(output2)[1], tf.shape(output2)[2]
        up3 = tf.image.resize(output3, [up_h, up_w], method='nearest')
        output2 = output2 + up3
        output2 = self.merge2(output2)

        up_h, up_w = tf.shape(output1)[1], tf.shape(output1)[2]
        up2 = tf.image.resize(output2, [up_h, up_w], method='nearest')
        output1 = output1 + up2
        output1 = self.merge1(output1)

        return output1, output2, output3


class SSH(tf.keras.layers.Layer):
    """Single Stage Headless Layer"""
    def __init__(self, out_channel, weight_decay, name='SSH', **kwargs):
        super(SSH, self).__init__(name=name, **kwargs)
        assert out_channel % 4 == 0
        activation = 'relu'
        if (out_channel <= 64):
            activation = 'lrelu'

        self.conv_3x3 = ConvUnit(filters=out_channel // 2, kernel_size=3, strides=1, weight_decay=weight_decay, activation=None)

        self.conv_5x5_1 = ConvUnit(filters=out_channel // 4, kernel_size=3, strides=1, weight_decay=weight_decay, activation=activation)
        self.conv_5x5_2 = ConvUnit(filters=out_channel // 4, kernel_size=3, strides=1, weight_decay=weight_decay, activation=None)

        self.conv_7x7_2 = ConvUnit(filters=out_channel // 4, kernel_size=3, strides=1, weight_decay=weight_decay, activation=activation)
        self.conv_7x7_3 = ConvUnit(filters=out_channel // 4, kernel_size=3, strides=1, weight_decay=weight_decay, activation=None)

        self.relu = ReLU()

    def call(self, x):
        conv_3x3 = self.conv_3x3(x)

        conv_5x5_1 = self.conv_5x5_1(x)
        conv_5x5 = self.conv_5x5_2(conv_5x5_1)

        conv_7x7_2 = self.conv_7x7_2(conv_5x5_1)
        conv_7x7 = self.conv_7x7_3(conv_7x7_2)

        output = tf.concat([conv_3x3, conv_5x5, conv_7x7], axis=3)
        output = self.relu(output)

        return output


class BboxHead(tf.keras.layers.Layer):
    """Bbox Head Layer"""
    def __init__(self, num_anchor, weight_decay, name='BboxHead', **kwargs):
        super(BboxHead, self).__init__(name=name, **kwargs)
        self.num_anchor = num_anchor
        self.conv = Conv2D(filters=num_anchor * 4, kernel_size=1, strides=1)

    def call(self, x):
        h, w = tf.shape(x)[1], tf.shape(x)[2]
        x = self.conv(x)

        return tf.reshape(x, [-1, h * w * self.num_anchor, 4])


class LandmarkHead(tf.keras.layers.Layer):
    """Landmark Head Layer"""
    def __init__(self, num_anchor, weight_decay, name='LandmarkHead', **kwargs):
        super(LandmarkHead, self).__init__(name=name, **kwargs)
        self.num_anchor = num_anchor
        self.conv = Conv2D(filters=num_anchor * 10, kernel_size=1, strides=1)

    def call(self, x):
        h, w = tf.shape(x)[1], tf.shape(x)[2]
        x = self.conv(x)

        return tf.reshape(x, [-1, h * w * self.num_anchor, 10])


class ClassHead(tf.keras.layers.Layer):
    """Class Head Layer"""
    def __init__(self, num_anchor, weight_decay, name='ClassHead', **kwargs):
        super(ClassHead, self).__init__(name=name, **kwargs)
        self.num_anchor = num_anchor
        self.conv = Conv2D(filters=num_anchor * 2, kernel_size=1, strides=1)

    def call(self, x):
        h, w = tf.shape(x)[1], tf.shape(x)[2]
        x = self.conv(x)

        return tf.reshape(x, [-1, h * w * self.num_anchor, 2])


def RetinaFaceModel(cfg, training=True, iou_th=0.4, score_th=0.02,name='RetinaFaceModel'):
    """Retina Face Model"""
    input_size = cfg['input_size'] if training else None
    weight_decay = 5e-4
    out_channel = 64
    num_anchor = 2
    backbone_type = cfg['backbone_type']

    # 인풋을 정의합니다.
    # shape = 640,640,3 if training
    x = inputs = Input([input_size,input_size, 3], name='input')

    # 특징추출기에 들어가는 사전학습모델의 전처리 함수를 적용합니다.
    x = tf.keras.applications.resnet.preprocess_input(x,name='preprocess')

    # 특징추출기 정의
    feature_extractor = MobileNetV2(input_shape=x.shape[1:], include_top=False, weights='imagenet')

    # 아웃풋의 레이어 인덱스 각 레이어의 shape는 순서대로 [80, 80, 32],[40, 40, 96],[20, 20, 160]
    output_layers = [54, 116, 143]

    # 특징 추출
    x = tf.keras.Model(
        inputs = [feature_extractor.input],
        ouputs = [feature_extractor.layers[i] for i in output_layers],
        name='feature_extractor')(x)

    # 특징 피라미드 맵 얻기
    fpn = FPN(out_channel=out_channel, weight_decay=weight_decay)(x)

    features = [SSH(out_channel=out_channel, weight_decay=weight_decay, name=f'SSH_{i}')(f)
                for i, f in enumerate(fpn)]

    bbox_regressions = tf.concat(
        [BboxHead(num_anchor, weight_decay=weight_decay, name=f'BboxHead_{i}')(f)
         for i, f in enumerate(features)], axis=1)
    landm_regressions = tf.concat(
        [LandmarkHead(num_anchor, weight_decay=weight_decay, name=f'LandmarkHead_{i}')(f)
         for i, f in enumerate(features)], axis=1)
    classifications = tf.concat(
        [ClassHead(num_anchor, weight_decay=weight_decay, name=f'ClassHead_{i}')(f)
         for i, f in enumerate(features)], axis=1)

    classifications = tf.keras.layers.Softmax(axis=-1)(classifications)

    if training:
        out = (bbox_regressions, landm_regressions, classifications)
    else:
        # only for batch size 1
        preds = tf.concat(  # [bboxes, landms, landms_valid, conf]
            [bbox_regressions[0], landm_regressions[0],
             tf.ones_like(classifications[0, :, 0][..., tf.newaxis]),
             classifications[0, :, 1][..., tf.newaxis]], 1)
        priors = prior_box_tf((tf.shape(inputs)[1], tf.shape(inputs)[2]),
                              cfg['min_sizes'],  cfg['steps'], cfg['clip'])
        decode_preds = decode_tf(preds, priors, cfg['variances'])

        selected_indices = tf.image.non_max_suppression(
            boxes=decode_preds[:, :4],
            scores=decode_preds[:, -1],
            max_output_size=tf.shape(decode_preds)[0],
            iou_threshold=iou_th,
            score_threshold=score_th)

        out = tf.gather(decode_preds, selected_indices)

    return Model(inputs, out, name=name)