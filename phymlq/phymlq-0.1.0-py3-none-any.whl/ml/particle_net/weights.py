import urllib


def load_weights(model):
    if model.name == 'particlenet-lite':
        urllib.request.urlretrieve(
            'https://github.com/Jai2500/particle-tagging/blob/master/phymlq/phymlq/ml/particle_net/weights-particlenet-lite.h5?raw=true',
            'weights_particlenet_lite.h5'
        )
        model.load_weights('weights_particlenet_lite.h5')
    else:
        # TODO: Train on ADA, Colab runs out of memory with the full model
        raise NotImplementedError('ParticleNet Full has not been trained yet.')