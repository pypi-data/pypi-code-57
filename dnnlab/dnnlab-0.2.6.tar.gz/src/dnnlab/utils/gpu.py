"""[summary]
"""
import tensorflow as tf


def info():
    """[summary]
    """
    print("Num GPUs Available: ",
          len(tf.config.experimental.list_physical_devices('GPU')))


def only_use_gpu(gpu_id, memory_growth=True):
    """[summary]
    Args:
        device ([type]): [description]
    """
    device = tf.config.list_physical_devices('GPU')[gpu_id]
    tf.config.experimental.set_visible_devices(device, 'GPU')
    if memory_growth:
        tf.config.experimental.set_memory_growth(device, True)
