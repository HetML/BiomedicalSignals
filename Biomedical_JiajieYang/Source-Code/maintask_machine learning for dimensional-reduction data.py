import pylab as pl
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import math
import random
from sklearn.externals import joblib
from sklearn.decomposition import PCA
import numpy as np
from keras.datasets import mnist
from keras.models import Model 
from keras.layers import Dense, Input
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.advanced_activations import PReLU
from keras.layers.convolutional import Convolution2D, MaxPooling2D, UpSampling2D
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, conv_utils
from six.moves import range
from keras.optimizers import Adam
import cv2
import random

with open('E:\python\maintask\maintask7\Training for auto.csv', 'r', ) as f:
	reader = csv.reader(f)
	rows0 = [row for row in reader]
	column = [row[1] for row in reader]
	a=len(rows0)
rows0=np.array(rows0)
rows0=rows0[:,1:len(rows0[0])-2]
rows0=rows0.astype(float)

with open('E:\python\maintask\maintask7\Training.csv', 'r', ) as f:
	reader = csv.reader(f)
	rows1 = [row for row in reader]
	column = [row[1] for row in reader]
	a=len(rows1)
rows1=np.array(rows1)

with open('E:\python\maintask\maintask7\Test5.csv', 'r', ) as g:
	reader = csv.reader(g)
	rows2 = [row for row in reader]
	column = [row[1] for row in reader]
	a=len(rows2)
rows2=np.array(rows2)


X=rows1[:,1:len(rows1[0])-2]
y=rows1[:,len(rows1[0])-1]
print(len(X))
X=X.astype(float)
y=y.astype(float)

M=rows2[:,1:len(rows1[0])-2]
M=M.astype(float)

for i in range(len(X)-1,-1,-1):
	if float(np.max(X[i])) < 50:
		X=np.delete(X,i,axis=0)
		y=np.delete(y,i,axis=0)

print(len(X))

a=list(range(len(X)))
slice = random.sample(a, len(a))
XX1=X[slice[1]]
yy1=y[slice[1]]
XX2=XX1
yy2=yy1
for j in range(2,len(slice)):
	if j<1.1*len(a):
		XX1=np.row_stack((XX1, X[slice[j]]))
		yy1=np.row_stack((yy1, y[slice[j]]))
	else:
		XX2=np.row_stack((XX2, X[slice[j]]))
		yy2=np.row_stack((yy2, y[slice[j]]))
		
print(len(rows0),len(rows0[0]))
		
input_img = Input(shape=(len(rows0[0]),))  # adapt this if using `channels_first` image data format

s = len(rows0[0])

x = Dense(s, activation='relu')(input_img)
encoded = Dropout(0.5)(x)
encoded = BatchNormalization(axis=-1, momentum=0.99, epsilon=0.00001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)(x)
encoded = Dense(1500, activation='softmax')(encoded)
encoded = Dropout(0.5)(encoded)
encoded = BatchNormalization(axis=-1, momentum=0.99, epsilon=0.00001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)(x)
encoded = Dense(750, activation='relu')(encoded)
encoded = Dropout(0.5)(encoded)
encoded = BatchNormalization(axis=-1, momentum=0.99, epsilon=0.00001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)(x)
encoded = Dense(350, activation='relu')(encoded)
encoded = BatchNormalization(axis=-1, momentum=0.99, epsilon=0.00001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)(x)
y = Dense(250, activation='relu')(x)
encoded = BatchNormalization(axis=-1, momentum=0.99, epsilon=0.00001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)(y)
decoded = Dense(350, activation='relu')(y)
encoded = BatchNormalization(axis=-1, momentum=0.99, epsilon=0.00001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)(x)
decoded = Dense(750, activation='relu')(decoded)
encoded = BatchNormalization(axis=-1, momentum=0.99, epsilon=0.00001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones', beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)(x)
decoded = Dense(1500, activation='sigmoid')(decoded)

z = Dense(s, activation='sigmoid')(decoded)
model = Model(input_img, z)
model.compile(optimizer='adam', loss='mse') # reporting the accuracy
model.fit(rows0, rows0, nb_epoch=10, batch_size=128, shuffle=True, validation_data=(rows0, rows0))

mid = Model(input_img, y)
reduced_representation0 = mid.predict(XX1)
reduced_representation1 = mid.predict(M)


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=10, max_features='auto', max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            n_estimators=10, n_jobs=1, oob_score=True, random_state=10,
            verbose=0, warm_start=False)
clf.fit(reduced_representation0, yy1)



k=0
for i in range(0,len(reduced_representation1)):
	print(clf.predict([reduced_representation1[i]]))
	if clf.predict([reduced_representation1[i]]) == 1:
		k=k+1
print(k, i)

