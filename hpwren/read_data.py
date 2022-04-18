#!/usr/bin/env python
# coding: utf-8

# Read and visualize the data after querying

import os
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.preprocessing import MinMaxScaler

def read_data_csv(file_path):
	"""
	Read from one csv file containing one-year data of a location
	
	Args:
		file_path: the path to the csv file to be read
	Returns:
		header: header of this file, list
		data: dictionary of exported data, np array under each key
	"""
	import csv
	data = {}
	with open(file_path, 'r', newline='') as incsv:
		reader = csv.reader(incsv, delimiter=',')
		header = next(reader)
		# add headers as keys in data dict
		for h in header:
			data[h] = []
		
		for row in reader:
			new_data = [float(d) for d in row]
			for i in range(len(header)):
				data[header[i]].append(new_data[i])

		for h in header:
			data[h] = np.array(data[h])

	return header, data

def read_data_dict(dir_path, years, loc_list):
	"""
	Read the data from csv and fill them into a dictionary

	Args:
		dir_path: the directory that contains raw HPWREN data
		years: list of years to read
		loc_list: list of locations to read, if it exists in the directory

	Return:
		data_dict: the dictionary contains the queried data
		loc_list: list of locations queried
	"""
	data_dict = {}
	for yr in years:
		year_path = os.path.join(dir_path, yr)
		loc_list_yr = [d for d in os.listdir(year_path) if
					   os.path.isdir(os.path.join(year_path, d))]
		if len(loc_list) > 0:  # find the intersection of all locations in
			# each year
			loc_list = set(loc_list).intersection(loc_list_yr)
		else:
			loc_list = loc_list_yr
		data_dict[yr] = {}
		for loc in loc_list:
			file_path = os.path.join(year_path, loc + '.csv')
			print('Reading file {}'.format(file_path))
			header, data = read_data_csv(file_path)
			data_dict[yr][loc] = data

	return data_dict, loc_list


def gen_new_series(data_dict, yr, location, features, st_idx, series_sample_num):
	new_series = []
	valid_series = True
	valid_sample_in_series = 0
	# init first-appear sample in the last_sample dictionary
	for fe in features:
		if fe not in gen_new_series.last_sample:
			gen_new_series.last_sample[fe] = 0.0

	# start constructing a new series
	for j in range(series_sample_num):
		# try to construct a new sample
		new_sample = []
		valid_sample = True
		for fe in features:
			if fe in data_dict[yr][location] and \
					not np.isnan(data_dict[yr][location][fe][st_idx + j]):
				gen_new_series.last_sample[fe] = data_dict[yr][location][fe][st_idx + j]
				new_sample.append(gen_new_series.last_sample[fe])
			else:
				# encounter n/a in the current sample thus invalid
				# cover the invalid value with previous samples
				valid_sample = False
				new_sample.append(gen_new_series.last_sample[fe])

		assert(len(new_sample) == len(features)), \
			'Incorrect length for new sample: should be {} but is {}'.format(
				len(features), len(new_sample))

		# increase the valid sample count if the current sample is valid
		valid_sample_in_series += valid_sample

		# append new sample (no matter valid or repeated) to the new series
		new_series.append(new_sample)

	assert(len(new_series) == series_sample_num), \
		'Incorrect length for new series: should be {} but is {}'.format(
			series_sample_num, len(new_series))

	# set the valid series flag to false if valid samples are less than a
	# certain proportion in this new series
	if valid_sample_in_series / (len(new_series) + 1) < gen_new_series.valid_ub:
		valid_series = False

	return new_series, valid_series

gen_new_series.last_sample = {}  # global previous sample of different features
gen_new_series.valid_ub = 0.6   # upper bound of valid sample proportion to
								# form a valid series

def gen_label(cur_hour, num_interval):
	if cur_hour < gen_label.start_hour:
		cur_hour += 24
	return np.int((cur_hour - gen_label.start_hour) / num_interval)

gen_label.start_hour = 0
gen_label.abnm_label = -1

def main():
	###############################
	# Import queried data
	###############################
	data_dict = {}
	dir_path = os.path.dirname(os.path.realpath(__file__))
	years = ['2018', '2019']

	for y in years:
		year_path = os.path.join(dir_path, y)
		loc_list = [d for d in os.listdir(year_path) if os.path.isdir(os.path.join(year_path, d))]
		data_dict[y] = {}
		for loc in loc_list:
			file_path = os.path.join(year_path, loc + '.csv')
			print('Reading file {}'.format(file_path))
			header, data = read_data_csv(file_path)
			data_dict[y][loc] = data

	pprint(data_dict.keys())
	pprint(data_dict['2018'].keys())

	###############################
	# Visualization
	###############################
	#dt_1st_day = datetime.datetime.strptime(year + '0101', '%Y%m%d')
	#dt_last_day = datetime.datetime.strptime(year + '1231', '%Y%m%d')
	#days_in_year = (dt_last_day - dt_1st_day).days + 1 # number of days in this year
	interval = 60 # number of minutes per sample after averaging
	day_sample_num = int(24*60/interval)
	# year_sample_num = int(days_in_year*24*60/interval)

	'''
	# Visualization 1: same time, diff locations
	year = '2018'
	loc1 = 'SY'
	loc2 = 'WS'
	days_num = 3
	st_idx, ed_idx = 0, day_sample_num*days_num
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111)
	plt.plot(data_dict[year][loc1]['Ta'][st_idx:ed_idx], \
			 data_dict[year][loc1]['Ua'][st_idx:ed_idx], \
			 label='Location {} y{} d0-{}'.format(loc1, year, days_num))
	plt.plot(data_dict[year][loc2]['Ta'][st_idx:ed_idx], \
			 data_dict[year][loc2]['Ua'][st_idx:ed_idx], \
			 label='Location {} y{} d0-{}'.format(loc2, year, days_num))
	ax1.set_xlabel('Temperature (°C)', fontsize=15)
	ax1.set_ylabel('Humidity (%)', fontsize=15)
	ax1.tick_params(labelsize=15)
	plt.legend(fontsize=15)
	plt.savefig('diffLoc.png', dpi=300)
	plt.show()

	# Visualization 2: same location, diff time
	year = '2018'
	loc = 'WS'
	days_diff = 180 # 3 months
	st_idx1, ed_idx1 = 0, day_sample_num*days_num
	st_idx2, ed_idx2 = day_sample_num*days_diff, day_sample_num*(days_diff+days_num)
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(111)
	plt.plot(data_dict[year][loc]['Ta'][st_idx1:ed_idx1], \
			 data_dict[year][loc]['Ua'][st_idx1:ed_idx1], \
			 label='Location {} y{} d0-{}'.format(loc, year, days_num))
	plt.plot(data_dict[year][loc]['Ta'][st_idx2:ed_idx2], \
			 data_dict[year][loc]['Ua'][st_idx2:ed_idx2], \
			 label='Location {} y{} d{}-{}'.format(loc, year, days_diff, days_diff+days_num))
	ax1.set_xlabel('Temperature (°C)', fontsize=15)
	ax1.set_ylabel('Humidity (%)', fontsize=15)
	ax1.tick_params(labelsize=15)
	plt.legend(fontsize=15)
	plt.savefig('diffTime.png', dpi=300)
	plt.show()

	# Visualization 3: same location, same time in two years
	year1 = '2018'
	year2 = '2019'
	loc = 'WS'
	st_idx, ed_idx = 0, day_sample_num*days_num
	fig3 = plt.figure()
	ax3 = fig3.add_subplot(111)
	plt.plot(data_dict[year1][loc]['Ta'][st_idx:ed_idx], \
			 data_dict[year1][loc]['Ua'][st_idx:ed_idx], \
			 label='Location {} y{} d0-{}'.format(loc, year1, days_num))
	plt.plot(data_dict[year2][loc]['Ta'][st_idx:ed_idx], \
			 data_dict[year2][loc]['Ua'][st_idx:ed_idx], \
			 label='Location {} y{} d0-{}'.format(loc, year2, days_num))
	ax3.set_xlabel('Temperature (°C)', fontsize=15)
	ax3.set_ylabel('Humidity (%)', fontsize=15)
	ax3.tick_params(labelsize=15)
	plt.legend(fontsize=15)
	plt.savefig('diffYear.png', dpi=300)
	plt.show()

	# Visualization 4: time series
	year1 = '2018'
	year2 = '2019'
	loc = 'SMERNS'
	days_num = 14
	st_idx, ed_idx = 0, day_sample_num*days_num
	fig4 = plt.figure()
	ax41 = fig4.add_subplot(211)
	plt.plot(np.arange(ed_idx-st_idx)/day_sample_num, \
			 data_dict[year1][loc]['Ta'][st_idx:ed_idx], \
			 label='Temp {} y{} d0-{}'.format(loc, year1, days_num))
	plt.plot(np.arange(ed_idx-st_idx)/day_sample_num, \
			 data_dict[year2][loc]['Ta'][st_idx:ed_idx], \
			 label='Temp {} y{} d0-{}'.format(loc, year2, days_num))
	ax41.set_xlabel('Days', fontsize=15)
	ax41.set_ylabel('Temperature (°C)', fontsize=15)
	ax41.tick_params(labelsize=15)
	plt.legend()

	ax42 = fig4.add_subplot(212)
	plt.plot(np.arange(ed_idx-st_idx)/day_sample_num, \
			 data_dict[year1][loc]['Ua'][st_idx:ed_idx], \
			 label='Humid {} y{} d0-{}'.format(loc, year1, days_num))
	plt.plot(np.arange(ed_idx-st_idx)/day_sample_num, \
			 data_dict[year2][loc]['Ua'][st_idx:ed_idx], \
			 label='Humid {} y{} d0-{}'.format(loc, year2, days_num))
	ax42.set_xlabel('Days', fontsize=15)
	ax42.set_ylabel('Humidity (%)', fontsize=15)
	ax42.tick_params(labelsize=15)
	plt.legend()

	plt.savefig('timeSerie.png', dpi=300)
	# plt.show()
	'''

	# Visualization 5: time series, diff location
	year = '2018'
	loc1 = 'PLC'
	loc2 = 'SY'
	days_num = 14
	st_idx, ed_idx = 0, day_sample_num*days_num
	fig5 = plt.figure()
	ax51 = fig5.add_subplot(211)
	plt.plot(np.arange(ed_idx-st_idx)/day_sample_num, \
			 data_dict[year][loc1]['Ta'][st_idx:ed_idx], \
			 label='Temp {} y{} d0-{}'.format(loc1, year, days_num))
	plt.plot(np.arange(ed_idx-st_idx)/day_sample_num, \
			 data_dict[year][loc2]['Ta'][st_idx:ed_idx], \
			 label='Temp {} y{} d0-{}'.format(loc2, year, days_num))
	ax51.set_xlabel('Days', fontsize=15)
	ax51.set_ylabel('Temperature (°C)', fontsize=15)
	ax51.tick_params(labelsize=15)
	plt.legend()

	ax52 = fig5.add_subplot(212)
	plt.plot(np.arange(ed_idx-st_idx)/day_sample_num, \
			 data_dict[year][loc1]['Ua'][st_idx:ed_idx], \
			 label='Humid {} y{} d0-{}'.format(loc1, year, days_num))
	plt.plot(np.arange(ed_idx-st_idx)/day_sample_num, \
			 data_dict[year][loc2]['Ua'][st_idx:ed_idx], \
			 label='Humid {} y{} d0-{}'.format(loc2, year, days_num))
	ax52.set_xlabel('Days', fontsize=15)
	ax52.set_ylabel('Humidity (%)', fontsize=15)
	ax52.tick_params(labelsize=15)
	plt.legend()

	plt.savefig('timeSeriediffLoc.png', dpi=300)
	plt.show()

	'''
	# Visualization 6: full time series
	data_dict = {}
	dir_path = './'
	years = ['2018', '2019', '2020']
	features = ['Dn', 'Dm', 'Dx', 'Sn', 'Sm', 'Sx', 'Ta', 'Ua', 'Pa', 'Ri']
	loc_list = []

	for yr in years:
		year_path = os.path.join(dir_path, yr)
		loc_list_yr = [d for d in os.listdir(year_path) if os.path.isdir(os.path.join(year_path, d))]
		if len(loc_list) > 0: # find the intersection of all locations in each year
			loc_list = set(loc_list).intersection(loc_list_yr)
		else:
			loc_list = loc_list_yr
		data_dict[yr] = {}
		for loc in loc_list:
			file_path = os.path.join(year_path, loc + '.csv')
			print('Reading file {}'.format(file_path))
			header, data = read_data_csv(file_path)
			data_dict[yr][loc] = data

	print('Location list after intersection:', loc_list)
	interval = 60  # number of minutes per sample after averaging
	day_sample_num = int(24 * 60 / interval)

	years = ['2018', '2019', '2020']
	f1, f2, f3 = 'Ta', 'Ua', 'Sx'
	for yr in years:
		for loc in loc_list:
			st_idx, ed_idx = 0, day_sample_num * 7
			fig = plt.figure()
			ax1 = fig.add_subplot(211)
			plt.plot(np.arange(ed_idx - st_idx) / day_sample_num,
					 data_dict[yr][loc][f1][st_idx:ed_idx],
					 label='{} {} y{} d{}-{}'.format(f1, loc, yr, int(st_idx/day_sample_num),
													   int(ed_idx/day_sample_num)))
			plt.plot(np.arange(ed_idx - st_idx) / day_sample_num,
					 data_dict[yr][loc][f2][st_idx:ed_idx],
					 label='{} {} y{} d{}-{}'.format(f2, loc, yr, int(st_idx/day_sample_num),
													   int(ed_idx/day_sample_num)))
			plt.plot(np.arange(ed_idx - st_idx) / day_sample_num,
					 data_dict[yr][loc][f3][st_idx:ed_idx],
					 label='{} {} y{} d{}-{}'.format(f3, loc, yr, int(st_idx/day_sample_num),
													   int(ed_idx/day_sample_num)))
			ax1.set_xlabel('Days', fontsize=15)
			ax1.tick_params(labelsize=15)
			plt.legend()

			st_idx, ed_idx = 0, day_sample_num * 365
			ax2 = fig.add_subplot(212)
			plt.plot(np.arange(ed_idx - st_idx) / day_sample_num,
					 data_dict[yr][loc][f1][st_idx:ed_idx],
					 label='{} {} y{} d{}-{}'.format(f1, loc, yr, int(st_idx/day_sample_num),
													   int(ed_idx/day_sample_num)))
			plt.plot(np.arange(ed_idx - st_idx) / day_sample_num,
					 data_dict[yr][loc][f2][st_idx:ed_idx],
					 label='{} {} y{} d{}-{}'.format(f2, loc, yr, int(st_idx/day_sample_num),
													   int(ed_idx/day_sample_num)))
			plt.plot(np.arange(ed_idx - st_idx) / day_sample_num,
					 data_dict[yr][loc][f3][st_idx:ed_idx],
					 label='{} {} y{} d{}-{}'.format(f3, loc, yr, int(st_idx/day_sample_num),
													   int(ed_idx/day_sample_num)))
			ax2.set_xlabel('Days', fontsize=15)
			ax2.tick_params(labelsize=15)
			plt.legend()

			plt.savefig('{}_{}.png'.format(yr, loc), dpi=300)
	'''

if __name__ == '__main__':
	main()