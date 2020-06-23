import tensorflow as tf

class TFCallbacks:
    def __init__(self):
        self.LOG_DIR = config.LOG_DIR
        self.CHECKPOINT_DIR = os.path.dirname(os.path.join(self.LOG_DIR, 'checkpoints/cp.ckpt'))
        
        config.CHECKPOINT_DIR = self.CHECKPOINT_DIR
        
    def checkpoint_logger(self):
        # Create a callback that saves the model's weights
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
                                                    filepath=self.CHECKPOINT_DIR,
                                                    save_weights_only=True,
                                                    verbose=1
                                                )
        
        return cp_callback
    
    def tesorboard_logger(self):
        
        return tf.keras.callbacks.TensorBoard(
                            log_dir=self.LOG_DIR, histogram_freq=0, write_graph=True, write_images=True,
                            update_freq='epoch', profile_batch=2, embeddings_freq=0,
                        )
