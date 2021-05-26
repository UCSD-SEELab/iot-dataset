# WESAD

**Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/WESAD+%28Wearable+Stress+and+Affect+Detection%29) 

**Task:** Classification of stress, normal, and amusement physiological states

**Number of instances:** 63000000

**Number of attributes:** 12

**Cite:** 

``` 
@article{schmidt2018wesad,
  title={Introducing WESAD, a Multimodal Dataset for Wearable Stress and Affect Detection},
  author={Schmidt, Philip and Reiss, Attila and Duerichen, Robert and Marberger, Claus and Van Laerhoven, Kristof},
  year={2018},
  isbn={9781450356923},
  publisher={Association for Computing Machinery},
  url={https://doi.org/10.1145/3242969.3242985},
  pages={400–408},
  booktitle={Proceedings of the 20th ACM International Conference on Multimodal Interaction},
  series={ICMI '18}
}
```

The samples are constructed using blood volume pulse, electrodermal activity, and temperature signals collected from a wearable device at 64hz, 4hz, and 4hz respectively.

## Get Started

Clone the [WESAD repo](https://github.com/WJMatthew/WESAD). Download this dataset [here](https://uni-siegen.sciebo.de/s/HGdUkoNlW1Ub0Gx) and run the command `python3 data_wrangling.py` to preprocess this dataset. In the preprocessing, 

- 30 second segments are extracted and independantly normalize for each subject's data
- EMG signals 
  - Are passed through a high pass filter to remove DC component before the mean and standard deviation are computed for 5 second segments
  - Then passed through a low pass filter and the signal segemented into 60 second windows, where feature peaks are computed
- RESP signal 
  -  Passed through a bandpass filter before computations



