#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import matplotlib.pyplot as plt

###############################################
# Data import functions
###############################################
def read_isolet(filename):
	x, y = [], []
	with open(filename, 'r') as f:
		lines = f.readlines()
		for line in lines:
			data = line.strip('.\n').split(',')
			new_y = int(data[-1])
			new_x = data[:-1]
			y.append(new_y)
			x.append(new_x)

	x, y = np.array(x), np.array(y)
	return x, y


def normalize_data(data, scaler_name='Standard'):
	if scaler_name == 'Robust':
		scaler = RobustScaler()

	elif scaler_name == 'Standard':
		scaler = StandardScaler()

	elif scaler_name == 'MinMax':
		scaler = MinMaxScaler(feature_range=(0, 1))

	scaled_data = scaler.fit_transform(
		np.reshape(data, (-1, data.shape[-1]))).reshape((-1,) + data.shape[1:])

	return scaled_data, scaler


###############################################
# Plot functions
###############################################
cat_cnt = 26  # number of categories

def get_cmap(n, name='hsv'):
	"""
	Returns a function that maps each index in 0, 1, ..., n-1 to a
	distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.
	"""
	return plt.cm.get_cmap(name, n + 2)

def plot_data(x, y, plot_3d=False, title='', fig_name=''):
	"""
	Plot scatter plot of the first 2/3 channels of x, with diff colors
	indicating diff classes, i.e., y

	Args:
		x: samples, (num_samples, num_features)
		y: labels, (num_samples,)
		plot_3d: if True, plot first 3 channels, else, plot first 2 channels
		title: title of plot, '' means no title
		fig_name: the name of the figure to be saved, '' means do not save
	"""
	scatter_size = 20

	fig = plt.figure()
	cmap = get_cmap(cat_cnt)
	if plot_3d:
		ax = fig.add_subplot(111, projection='3d')  # 3-D
	else:
		ax = fig.add_subplot(111)  # 2-D
	for i in range(cat_cnt):
		mask = (y == i)
		if plot_3d:
			# z = np.arange(len(mask))[mask] # get the time index
			ax.scatter(x[mask, 0], x[mask, 1], x[mask, 2], alpha=0.8,
					   color=cmap(i), s=scatter_size, label=str(i))  # 3-D
		else:
			ax.scatter(x[mask, 0], x[mask, 1], alpha=0.8, color=cmap(i),
					   s=scatter_size, label=str(i))  # 2-D
	ax.set_xlabel('Attribute 0', fontsize=15)
	ax.set_ylabel('Attribute 1', fontsize=15)
	ax.tick_params(labelsize=15)
	if title != '':
		ax.set_title(title, fontsize=15)
	fig.legend()
	plt.grid()
	plt.tight_layout()

	if fig_name != '':
		plt.savefig(fig_name, dpi=300, bbox_inches='tight')
	plt.show()


def pca_plot_data(x, y, plot_3d=False, title='', fig_name=''):
	"""
	Plot scatter plot of the first 2/3 channels of x after PCA,
	with diff colors indicating diff classes, i.e., y

	Args:
		x: samples, (num_samples, num_features)
		y: labels, (num_samples,)
		plot_3d: if True, plot first 3 channels, else, plot first 2 channels
		title: title of plot, '' means no title
		fig_name: the name of the figure to be saved, '' means do not save
	"""
	from sklearn.decomposition import PCA
	scatter_size = 20

	pca = PCA(n_components=3)
	pc_x = pca.fit_transform(x)
	print('explained_variance_ratio_: {}'.format(pca.explained_variance_ratio_))

	# scatter plot
	fig = plt.figure()
	cmap = get_cmap(cat_cnt)
	if plot_3d:
		ax = fig.add_subplot(111, projection='3d')  # 3-D
	else:
		ax = fig.add_subplot(111)
	for i in range(cat_cnt):
		mask = (y == i)
		if plot_3d:
			# z = np.arange(len(mask))[mask] # get the time index
			ax.scatter(pc_x[mask, 0], pc_x[mask, 1], pc_x[mask, 2], alpha=0.8,
					   color=cmap(i), s=scatter_size, label=str(i))  # 3-D
		else:
			ax.scatter(pc_x[mask, 0], pc_x[mask, 1], alpha=0.8, color=cmap(i),
					   s=scatter_size, label=str(i))  # 2-D
	ax.set_xlabel('Principal Component 0', fontsize=15)
	ax.set_ylabel('Principal Component 1', fontsize=15)
	ax.tick_params(labelsize=15)
	if title != '':
		ax.set_title(title, fontsize=15)
	fig.legend()
	plt.grid()
	plt.tight_layout()

	if fig_name != '':
		plt.savefig(fig_name, dpi=300, bbox_inches='tight')
	plt.show()


def main():
	# read training data
	X_train, y_train = read_isolet('isolet1+2+3+4.data')
	print(X_train.shape, y_train.shape)

	# normalize training data
	X_train, scaler = normalize_data(X_train)

	# read test data
	X_test, y_test = read_isolet('isolet5.data')
	print(X_test.shape, y_test.shape)
	X_test = scaler.transform(X_test)

	##########################################
	# Scatter plots
	##########################################
	plot_data(X_train[:100], y_train[:100], plot_3d=False)
	plot_data(X_test[:100], y_test[:100], plot_3d=False)

	##########################################
	# PCA plots
	##########################################
	pca_plot_data(X_train[:100], y_train[:100], plot_3d=False)
	pca_plot_data(X_test[:100], y_test[:100], plot_3d=False)


if __name__ == '__main__':
	main()