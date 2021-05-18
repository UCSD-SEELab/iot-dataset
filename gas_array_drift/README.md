# Gas Sensor Array Drift Dataset

**Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Gas+Sensor+Array+Drift+Dataset+at+Different+Concentrations)

**Tasks:** Classification, regression, clustering, etc.

**Number of instances:** 13910

**Number of Attributes:** 129

**Cite:** 

```
@article{vergara2012chemical,
  title={Chemical gas sensor drift compensation using classifier ensembles},
  author={Vergara, Alexander and Vembu, Shankar and Ayhan, Tuba and Ryan, Margaret A and Homer, Margie L and Huerta, Ram{\'o}n},
  journal={Sensors and Actuators B: Chemical},
  volume={166},
  pages={320--329},
  year={2012},
  publisher={Elsevier}
}
```

This data set contains 13,910 measurements from 16 chemical sensors exposed to 6 gases at different concentration levels. The experiment spans 36 months thus the effects of sensor drift is included. This dataset is an extension of the Gas Sensor Array Drift Dataset ([Web Link](http://archive.ics.uci.edu/ml/datasets/Gas+Sensor+Array+Drift+Dataset)), providing now the information about the concentration level at which the sensors were exposed for each measurement. 

## Getting Started

* Download the dataset from UCI's repository and put all `.dat` files in this directory
* Run `python3 read_gas.py` to import data and visualize. Need `numpy, matplotlib` and `sklearn.preprocessing`.

