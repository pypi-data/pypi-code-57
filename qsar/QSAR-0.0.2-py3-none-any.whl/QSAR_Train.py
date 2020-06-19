temp_encoder.trainable = False
# checkpoint
filepath="/content/drive/Shared drives/Juvena R&D/R&D/Machine Learning/Phase_1_QSAR/weights/test" + "weights_nn_classifier_tanh.hdf5"
loss = []
val_loss = []

batch_feat = []
batch_label = []

######## Data
pos_uniprot = dat.pos_uniprot
neg_uniprot = dat.neg_uniport
data = dat.all_secreted_data



for i in range(0,9):
    if i < 8:
        positives = pos_uniprot[i*10:(i+1)*10]
    else:# if = 8
        positives = pos_uniprot[80:]
    pos_feat = data[data['Uniprot'].isin(positives)].drop(labels=['Uniprot'],axis=1)
    batch_feat += [pos_feat.append(data[data['Uniprot'].isin(neg_uniprot)].drop(labels=['Uniprot'],axis=1))]
    label = pd.Series(data = np.ones(len(pos_feat))).append(pd.Series(data = np.zeros(10)))
    batch_label += [label.to_numpy()]

# print(batch_feat[0].shape)
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=False, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
classifiers = []

for i, (batch_data, label) in enumerate(zip(batch_feat, batch_label)):
    print("="*10)
    print("training",str(i),"th","model")
    #Reinitializing weights
    clf = classifier.classifier

    #Reshaping array for convolutional autoencoder
    batch_data = np.concatenate([np.zeros((batch_data.shape[0],53)), batch_data, np.zeros((batch_data.shape[0],54))], axis=1)
    batch_data = batch_data.reshape(batch_data.shape[0], batch_data.shape[1], 1)

    #Find embeddings of training set from encoder
    latent = temp_encoder.predict(batch_data)
    latent = latent.reshape((latent.shape[0],-1))

    shuffle_idx = np.random.permutation(latent.shape[0])

    #Find embeddings of test set from encoder
    # latent_t = encoder.predict(custom_data[test_index])
    # latent_t = latent_t.reshape((latent_t.shape[0],-1))

    class_weight = [1, 1]

    history = clf.fit(latent[shuffle_idx],label[shuffle_idx], 
                      callbacks=callbacks_list,
                      epochs=50, class_weight=class_weight)

    loss += [history.history['loss']]

    classifiers.append(clf)