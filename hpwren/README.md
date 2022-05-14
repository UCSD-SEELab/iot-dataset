# HPWREN Sensor Dataset

**Source:** [HPWREN Raw Sensor Data](http://hpwren.ucsd.edu/TM/Sensors/Data/)

**Tasks:** N/A

This directory provides scripts to query and pre-process raw sensor data from HPWREN website. The raw sensor data is sampled per hour and includes the following readings:

| Reading                              | Value  | Unit           | Label |
| ------------------------------------ | ------ | -------------- | ----- |
| Wind direction minimum               | 286    | degrees        | Dn    |
| Wind direction average               | 288    | degrees        | Dm    |
| Wind direction maximum               | 290    | degrees        | Dx    |
| Wind speed minimum                   | 2.9    | m/sec          | Sn    |
| Wind speed average                   | 3.0    | m/sec          | Sm    |
| Wind speed maximum                   | 3.0    | m/sec          | Sx    |
| Air temperature                      | 16.2   | Celsius        | Ta    |
| Relative humidity                    | 34.8   | percent        | Ua    |
| Air pressure (not altitude adjusted) | 879.4  | hPa (millibar) | Pa    |
| Rain accumulation                    | 123.21 | mm             | Rc    |
| Supplied voltage                     | 25.3   | Volt           | Vs    |

## Getting Started

* Init a Python virtual environment and install necessary packages

  ```bash
  python3 -m venv .hpwren
  source .hpwren/bin/activate
  pip3 install -r requirements.txt
  ```

* Run `python3 query_data.py` to query the data of certain years and certain sensors to .csv files.
  Make sure to update the line 114-118:

  ```python
  baseURL = "http://hpwren.ucsd.edu/TM/Sensors/Data/"
  year = ['2021'] # year of data to request
  
  filePattern = ":0R0:4:0"
  header = ['t', 'Dn', 'Dm', 'Dx', 'Sn', 'Sm', 'Sx', 'Ta', 'Ua', 'Pa', 'Rc', 'Rd', 'Ri'] # type of sensor readings to request
  ```

  and line 169:

  ```python
  all_header = ['year', 'month', 'day', 'hour', 'Dn', 'Dm', 'Dx', 'Sn',
                'Sm', 'Sx', 'Ta', 'Ua', 'Pa', 'Rc', 'Rd', 'Ri']
  ```

  The query process may take 1-2 hours. All downloaded data will be stored in the folders named by the year, e.g., a folder named '2021'.

* (Optional) Test ARIMA model with `test_arima.ipynb`.

* (Optional) Test RNN, LSTM, GRU, CNN, MLP with `test_lstm.py`. The part is contributed by [Xiyuan Zhang](https://xiyuanzh.github.io/).

* (Optional) Use `read_data.py` to generate dataset for Federated Learning, following the same format as the [LEAF dataset](https://leaf.cmu.edu/).

  * `--tf` := fraction of data in training set, written as a decimal; default is 0.9
  * `--ws` := window size of data, int; default is 24, where the first 23 samples are used as input and the last sample is used as the ground-truth target.