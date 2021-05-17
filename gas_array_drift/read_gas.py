#!/usr/bin/env python
# coding: utf-8

import numpy as np

###############################################
# Data import functions
###############################################
def read_gas_data(filename):
	x, y = [], []
	with open(filename, 'r') as f:
		lines = f.readlines()
		for line in lines:
			data = line.strip().split()
			new_y = int(data[0]) - 1
			new_x = [float(d.split(':')[1]) for d in data[1:]]
			y.append(new_y)
			x.append(new_x)

	x, y = np.array(x), np.array(y)
	return x, y


###############################################
# Plot functions
###############################################
cat_cnt = 6  # number of categories
labels = ['Ethanol', 'Ethylene', 'Ammonia', 'Acetaldehyde', 'Acetone',
		  'Toluene']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
		  'tab:brown']


def plot_gas_data(x, y, plot_3d=False, title='', fig_name=''):
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
	import matplotlib.pyplot as plt
	scatter_size = 20

	fig = plt.figure()
	if plot_3d:
		ax = fig.add_subplot(111, projection='3d')  # 3-D
	else:
		ax = fig.add_subplot(111)  # 2-D
	for i in range(cat_cnt):
		mask = (y == i)
		if plot_3d:
			# z = np.arange(len(mask))[mask] # get the time index
			ax.scatter(x[mask, 0], x[mask, 1], x[mask, 2], alpha=0.8,
					   color=colors[i], s=scatter_size, label=labels[i])  # 3-D
		else:
			ax.scatter(x[mask, 0], x[mask, 1], alpha=0.8, color=colors[i],
					   s=scatter_size, label=labels[i])  # 2-D
	ax.set_xlabel('Channel 0', fontsize=15)
	ax.set_ylabel('Channel 1', fontsize=15)
	ax.tick_params(labelsize=15)
	if title != '':
		ax.set_title(title, fontsize=15)
	# legend = fig.legend()
	plt.grid()
	plt.tight_layout()

	if fig_name != '':
		plt.savefig(fig_name, dpi=300, bbox_inches='tight')
	plt.show()


def pca_plot_gas_data(x, y, plot_3d=False, title='', fig_name=''):
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
	import matplotlib.pyplot as plt
	from sklearn.decomposition import PCA
	scatter_size = 20

	pca = PCA(n_components=3)
	pc_x = pca.fit_transform(x)
	print('explained_variance_ratio_: {}'.format(pca.explained_variance_ratio_))

	# scatter plot
	fig = plt.figure()
	if plot_3d:
		ax = fig.add_subplot(111, projection='3d')  # 3-D
	else:
		ax = fig.add_subplot(111)
	for i in range(cat_cnt):
		mask = (y == i)
		if plot_3d:
			# z = np.arange(len(mask))[mask] # get the time index
			ax.scatter(pc_x[mask, 0], pc_x[mask, 1], pc_x[mask, 2], alpha=0.8,
					   color=colors[i], s=scatter_size, label=labels[i])  # 3-D
		else:
			ax.scatter(pc_x[mask, 0], pc_x[mask, 1], alpha=0.8, color=colors[i],
					   s=scatter_size, label=labels[i])  # 2-D
	ax.set_xlabel('Principal Component 0', fontsize=15)
	ax.set_ylabel('Principal Component 1', fontsize=15)
	ax.tick_params(labelsize=15)
	if title != '':
		ax.set_title(title, fontsize=15)
	legend = fig.legend()
	plt.grid()
	plt.tight_layout()

	if fig_name != '':
		plt.savefig(fig_name, dpi=300, bbox_inches='tight')
	plt.show()


def plot_gas_data_compare(x, y, y_hat, title='', fig_name=''):
	"""
	Plot scatter plot of the first 2 channels of X, compare with the
	ground-truth labels

	Args:
		x: samples, (num_samples, num_features)
		y: ground-truth labels, (num_samples,)
		y_hat: predicted labels, (num_sample,)
		title: title of plot, '' means no title
		fig_name: the name of the figure to be saved, '' means do not save
	"""
	import matplotlib.pyplot as plt
	scatter_size = 20

	fig = plt.figure(figsize=(9, 4))
	ax1 = fig.add_subplot(121)  # 2-D
	for i in range(cat_cnt):
		mask = (y == i)
		ax1.scatter(x[mask, 0], x[mask, 1], alpha=0.8, color=colors[i],
					s=scatter_size, label=labels[i])  # 2-D
	ax1.set_xlabel('Channel 0', fontsize=15)
	ax1.set_ylabel('Channel 1', fontsize=15)
	ax1.tick_params(labelsize=15)
	ax1.set_title('ground truth', fontsize=15)
	plt.grid()

	ax2 = fig.add_subplot(122)  # 2-D
	for i in range(cat_cnt):
		mask = (y_hat == i)
		ax2.scatter(x[mask, 0], x[mask, 1], alpha=0.8, color=colors[i],
					s=scatter_size)  # 2-D
	ax2.set_xlabel('Channel 0', fontsize=15)
	ax2.set_ylabel('Channel 1', fontsize=15)
	ax2.tick_params(labelsize=15)
	if title != '':
		ax2.set_title(title, fontsize=15)
	legend = fig.legend(fontsize=12, loc='upper center', ncol=6,
						bbox_to_anchor=(0.5, 1.1))
	plt.grid()
	plt.tight_layout()

	if fig_name != '':
		plt.savefig(fig_name, dpi=300, bbox_inches='tight')
	plt.show()


def main():
	##########################################
	# Read and Plot
	##########################################
	plot_3d = False

	# read batch 1
	x1, y1 = read_gas_data('batch1.dat')
	print(x1.shape, y1.shape)

	# normalize x along each dimension in this batch to between (-1, 1)
	x1max = np.amax(x1, axis=0)
	x1mean = np.mean(x1, axis=0)
	x1min = np.amin(x1, axis=0)
	x1scale = 1 / np.maximum(x1max - x1mean, x1mean - x1min)
	x1 = (x1 - x1mean) * x1scale

	# read batch10 and normalize the same as batch1
	x10, y10 = read_gas_data('batch10.dat')
	x10 = (x10 - x1mean) * x1scale

	##########################################
	# Scatter plots
	##########################################
	plot_gas_data(x1, y1, plot_3d=plot_3d)
	plot_gas_data(x10, y10, plot_3d=plot_3d)

	##########################################
	# PCA plots
	##########################################
	pca_plot_gas_data(x1, y1, plot_3d=plot_3d)
	pca_plot_gas_data(x10, y10, plot_3d=plot_3d)


if __name__ == '__main__':
	main()