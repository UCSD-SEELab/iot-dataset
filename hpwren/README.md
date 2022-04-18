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

  The query process make take 1-2 hours.

* 