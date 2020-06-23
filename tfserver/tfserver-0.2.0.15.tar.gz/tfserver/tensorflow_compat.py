import tensorflow

if tensorflow.__version__ [0] == '1':
    try:
        from tensorflow.contrib import lite
    except SyntaxError:
        pass
    else:
        tensorflow.lite = lite
    tf = tensorflow

else:
    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior ()
