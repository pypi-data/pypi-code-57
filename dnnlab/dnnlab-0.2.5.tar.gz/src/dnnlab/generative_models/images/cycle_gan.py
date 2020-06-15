# Copyright 2019 Tobias Höfer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""The code is written using the Keras Sequential API with a tf.GradientTape
training loop. This module implements the minmax game used to train a cylce GAN.

Generative Adversarial Networks (GANs) are one of the most interesting ideas in
computer science today. Two models are trained simultaneously by an adversarial
process. A generator("the artist") learns to create images that look real, while
a discriminator ("the art critic") learns to tell real images apart from fakes.
"""
from datetime import datetime
import time
import os
import logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # FATAL
logging.getLogger("tensorflow").setLevel(logging.FATAL)

import tensorflow as tf

from dnnlab.errors.dnnlab_exceptions import ModelNotCompiledError


class CycleGAN(object):
    """Implements a cylce gan learning model.

    Attributes:
        generator_target (keras.model): Generates target images from source.
        generator_source(keras.model): Generates source images from targets.
        discriminator_target (keras.model): Compares fake targets to real ones.
        discriminator_source(keras.model): Compares fake sources to real ones.
        generator_target_optimizer (keras.optimizer): Optimization alg for
            generator_target.
        generator_source_optimizer (keras.optimizer): Optimization alg for
            generator_source.
        discriminator_target_optimizer (keras.optimizer): Optimization alg for
            discriminator_target.
        discriminator_source_optimizer (keras.optimizer): Optimization alg for
            discriminator_source.
        init_timestamp (str): Acts as a unique folder identifier.
        logdir (str): Top level logdir.
        tensorboard (str): Path to tensorboard summary files.
        ckpt_dir (str): Path to ckpt files.
        ckpt_manager (tf.train.CheckpointManager): Deletes old checkpoints.
        checkpoint (tf.train.Checkpoint): Groups trackable objects, saving and
            restoring them.
    """
    def __init__(self, generator_target, generator_source,
                 discriminator_target, discriminator_source):
        """Takes four keras.models that take part in the cycling gan game.

        Args:
            generator_target (keras.model): Generates target imgs from sources.
            generator_source(keras.model): Generates source imgs from targets.
            discriminator_target(keras.model): Compares fake/real targets.
            discriminator_source(keras.model): Compares fake/real sources.
        """
        self.generator_target = generator_target
        self.generator_source = generator_source
        self.discriminator_target = discriminator_target
        self.discriminator_source = discriminator_source
        self.generator_target_optimizer = None
        self.generator_source_optimizer = None
        self.discriminator_target_optimizer = None
        self.discriminator_source_optimizer = None
        self.init_timestamp = "CycleGAN-" + datetime.now().strftime(
            "%d%m%Y-%H%M%S")
        self.logdir = os.path.join("logs", self.init_timestamp)
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        self.ckpt_manager = None
        self.checkpoint = None

    def compile(self,
                optimizer="adam",
                lr_gen_target=1e-4,
                lr_gen_source=1e-4,
                lr_disc_target=1e-4,
                lr_disc_source=1e-4):
        """Defines the optimization part of the learning algorithm to our
        learning model.

        Args:
            optimizer (str, optional): [description]. Defaults to "adam".
            lr_gen_g ([type], optional): [description]. Defaults to 1e4.
            lr_gen_f ([type], optional): [description]. Defaults to 1e4.
            lr_disc_y ([type], optional): [description]. Defaults to 1e4.
            lr_disc_x ([type], optional): [description]. Defaults to 1e4.
        """
        if optimizer == "adam":
            self.generator_target_optimizer = tf.keras.optimizers.Adam(
                lr_gen_target)
            self.generator_source_optimizer = tf.keras.optimizers.Adam(
                lr_gen_source)
            self.discriminator_target_optimizer = tf.keras.optimizers.Adam(
                lr_disc_target)
            self.discriminator_source_optimizer = tf.keras.optimizers.Adam(
                lr_disc_source)

        if self.checkpoint is None:
            self.checkpoint = tf.train.Checkpoint(
                generator_target=self.generator_target,
                generator_source=self.generator_source,
                discriminator_target=self.discriminator_target,
                discriminator_source=self.discriminator_source,
                generator_target_optimizer=self.generator_target_optimizer,
                generator_source_optimizer=self.generator_source_optimizer,
                discriminator_target_optimizer=self.
                discriminator_target_optimizer,
                discriminator_source_optimizer=self.
                discriminator_source_optimizer)
            self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                           self.ckpt_dir,
                                                           max_to_keep=5)

    def fit(self,
            source_domain,
            target_domain,
            epochs,
            save_ckpt=5,
            verbose=1,
            max_outputs=2,
            initial_step=0):
        """Trains all four models for n EPOCHS. Saves ckpts every n EPOCHS.
        The training loop together with the optimization algorithm define the
        learning algorithm.

        Args:
            source_domain (tf.dataset): Images that generator sees as source
                with shape(None, width, height, depth).
            target_domain (tf.dataset): Images that generator tries to translate
                to with shape(None, width, height, depth).
            epochs (int): Number of epochs.
            save_ckpt (int): Save ckpts every n Epochs.
            verbose (int, optional): Keras Progbar verbose lvl. Defaults to 1.
            max_outputs (int, optional): Number of images shown in TB.
                Defaults to 2.
            initial_step (int): Step at which to start training. Useful for
                resuming a previous run.


        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """
        if self.generator_target_optimizer is None:
            raise ModelNotCompiledError("use CycleGAN.compile() first.")

        # Retrace workaround @function signature only tensors.
        step = tf.Variable(initial_step, name="step", dtype=tf.int64)

        num_batches = tf.data.experimental.cardinality(source_domain).numpy()
        # Keras Progbar
        progbar = tf.keras.utils.Progbar(target=num_batches, verbose=verbose)
        file_writer = tf.summary.create_file_writer(self.tensorboard)
        file_writer.set_as_default()
        for epoch in range(epochs):
            step_float = 0
            start = time.time()
            for source_images, target_images in zip(source_domain,
                                                    target_domain):
                self.train_step(source_images, target_images, step,
                                max_outputs, file_writer)
                file_writer.flush()
                progbar.update(current=(step_float))
                step_float += 1
                step.assign(step + 1)

            # Save the model every n epochs
            if (epoch + 1) % save_ckpt == 0:
                ckpt_save_path = self.ckpt_manager.save()
                print("\nSaving checkpoint for epoch {} at {}".format(
                    epoch + 1, ckpt_save_path))

            print(" - Epoch {} finished in {} sec\n".format(
                epoch + 1, int(time.time() - start)))

    def restore(self, ckpt_path):
        """Restore model weights from the latest checkpoint.

        Args:
            ckpt_path (str): Relative path to ckpt files.

        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """

        restore_path = os.path.dirname(ckpt_path)
        self.logdir = restore_path
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        if self.ckpt_manager is None:
            raise ModelNotCompiledError("use cycleGAN.compile() first.")
        self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                       self.ckpt_dir,
                                                       max_to_keep=5)
        # if a checkpoint exists, restore the latest checkpoint.
        if self.ckpt_manager.latest_checkpoint:
            self.checkpoint.restore(self.ckpt_manager.latest_checkpoint)
            print("Latest checkpoint restored!!")
        else:
            print("Can not find ckpt files at {}".format(ckpt_path))

    def export(self, model_format="hdf5"):
        """Exports the trained models in hdf5 or SavedModel format.

        Args:
            model_format (str, optional): SavedModel or HDF5. Defaults to hdf5.
        """
        model_dir = os.path.join(self.logdir, "models")
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if model_format == "hdf5":
            self.generator_target.save(
                os.path.join(model_dir, "generator_target.h5"))
            self.generator_source.save(
                os.path.join(model_dir, "generator_source.h5"))
            self.discriminator_target.save(
                os.path.join(model_dir, "discriminator_target.h5"))
            self.discriminator_source.save(
                os.path.join(model_dir, "discriminator_source.h5"))

        elif model_format == "SavedModel":
            self.generator_target.save(
                os.path.join(model_dir, "generator_target"))
            self.generator_source.save(
                os.path.join(model_dir, "generator_source"))
            self.discriminator_target.save(
                os.path.join(model_dir, "discriminator_target"))
            self.discriminator_source.save(
                os.path.join(model_dir, "discriminator_source"))

    @tf.function
    def train_step(self, source_images, target_images, step, max_outputs,
                   file_writer):
        """Decorated function (@tf.function) that creates a callable tensorflow
        graph from a python function.
        """
        with file_writer.as_default():
            # Record gradients for generator and discriminator for each seperate
            # training step.
            with tf.GradientTape(persistent=True) as tape:
                tf.summary.image("target_images",
                                 target_images,
                                 step=step,
                                 max_outputs=max_outputs)
                tf.summary.image("source_images",
                                 source_images,
                                 step=step,
                                 max_outputs=max_outputs)
                generated_target_images = self.generator_target(source_images,
                                                                training=True)
                tf.summary.image("generated_target_images",
                                 generated_target_images,
                                 step=step,
                                 max_outputs=max_outputs)
                cycled_source_images = self.generator_source(
                    generated_target_images, training=True)
                tf.summary.image("cycled_source_images",
                                 cycled_source_images,
                                 step=step,
                                 max_outputs=max_outputs)

                generated_source_images = self.generator_source(target_images,
                                                                training=True)
                tf.summary.image("generated_source_images",
                                 generated_source_images,
                                 step=step,
                                 max_outputs=max_outputs)
                cycled_target_images = self.generator_target(
                    generated_source_images, training=True)
                tf.summary.image("cycled_target_images",
                                 cycled_target_images,
                                 step=step,
                                 max_outputs=max_outputs)

                # same_source and same_target are used for identity loss.
                same_source = self.generator_source(target_images,
                                                    training=True)
                same_target = self.generator_target(source_images,
                                                    training=True)

                disc_real_source = self.discriminator_source(source_images,
                                                             training=True)
                disc_real_target = self.discriminator_target(target_images,
                                                             training=True)

                disc_fake_source = self.discriminator_source(
                    generated_source_images, training=True)
                disc_fake_target = self.discriminator_target(
                    generated_target_images, training=True)

                # Calculate the adversarial loss.
                gen_target_loss = self.generator_loss(disc_fake_target)
                gen_source_loss = self.generator_loss(disc_fake_source)

                # Calculate the cycle loss
                total_cycle_loss = self.cycle_loss(
                    source_images, cycled_source_images) + self.cycle_loss(
                        target_images, cycled_target_images)

                # Total gen loss = adversarial + cycle + identity
                total_gen_target_loss = gen_target_loss + total_cycle_loss + self.identity_loss(
                    target_images, same_target)

                total_gen_source_loss = gen_source_loss + total_cycle_loss + self.identity_loss(
                    source_images, same_source)

                tf.summary.scalar("gen_target_loss",
                                  total_gen_target_loss,
                                  step=step)
                tf.summary.scalar("gen_source_loss",
                                  total_gen_source_loss,
                                  step=step)

                # Total discriminator loss.
                disc_source_loss = self.discriminator_loss(
                    disc_real_source, disc_fake_source)
                disc_target_loss = self.discriminator_loss(
                    disc_real_target, disc_fake_target)
                tf.summary.scalar("disc_source_loss",
                                  disc_source_loss,
                                  step=step)
                tf.summary.scalar("disc_target_loss",
                                  disc_target_loss,
                                  step=step)

            gradients_of_generator_target = tape.gradient(
                total_gen_target_loss,
                self.generator_target.trainable_variables)
            gradients_of_generator_source = tape.gradient(
                total_gen_source_loss,
                self.generator_source.trainable_variables)
            gradients_of_discriminator_target = tape.gradient(
                disc_target_loss,
                self.discriminator_target.trainable_variables)
            gradients_of_discriminator_source = tape.gradient(
                disc_source_loss,
                self.discriminator_source.trainable_variables)

            self.generator_target_optimizer.apply_gradients(
                zip(gradients_of_generator_target,
                    self.generator_target.trainable_variables))
            self.generator_source_optimizer.apply_gradients(
                zip(gradients_of_generator_source,
                    self.generator_source.trainable_variables))
            self.discriminator_target_optimizer.apply_gradients(
                zip(gradients_of_discriminator_target,
                    self.discriminator_target.trainable_variables))
            self.discriminator_source_optimizer.apply_gradients(
                zip(gradients_of_discriminator_source,
                    self.discriminator_source.trainable_variables))

    @staticmethod
    def discriminator_loss(real, generated):
        """This method quantifies how well the discriminator is able to
        distinguish real images from fakes. It compares the discriminator's
        predictions on real images to an array of 1s, and the discriminator's
        predictions on fake (generated) images to an array of 0s.

        Args:
            real_image ([type]): [description]
            generated_image ([type]): [description]
        """
        # This method returns a helper function to compute cross entropy loss.
        cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        # Compares real images to tensors of 1 -> if real output 1s
        real_loss = cross_entropy(tf.ones_like(real), real)
        # Compares generated images to tensors of 0 -> if generated output 0s
        fake_loss = cross_entropy(tf.zeros_like(generated), generated)

        total_loss = real_loss + fake_loss
        return total_loss * 0.5

    @staticmethod
    def generator_loss(generated):
        """The generator's loss quantifies how well it was able to trick the
           discriminator. Intuitively, if the generator is performing well, the
           discriminator will classify the generated images as real (or 1).
           Here, we will compare the discriminators decisions on the generated
           images to an array of 1s.
        """
        # This method returns a helper function to compute cross entropy loss.
        cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        return cross_entropy(tf.ones_like(generated), generated)

    @staticmethod
    def cycle_loss(real_image, cycled_image):
        """Cycle consistency means the result should be close to the original
        source. For example, if one translates a sentence from English to French,
        and then translates it back from French to English, then the resulting
        sentence should be the same as the original sentence.
        """
        return tf.reduce_mean(tf.abs(real_image - cycled_image))

    @staticmethod
    def identity_loss(real_image, same_image):
        """[summary]
        """
        loss = tf.reduce_mean(tf.abs(real_image - same_image))
        return loss * 0.5
