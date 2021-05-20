# Wifi-CSI Dataset

**Source:** [A Survey on Behaviour Recognition Using WiFi Channel State Information](http://ieeexplore.ieee.org/document/8067693/)

**Task:** Classification of passive human behavior (lay down, fall, run, etc)

**Number of instances:** 

**Number of attributes:** 

**Cite:**

```
```



To create the samples, 6 people were recorded doing 6 activities ((lay down, fall , walk, run, sit down, stand up) for 20 seconds, with 20 trials of each acitivity per person. The Rx (commercial Intel 5300 NIC) sampled at a rate of 1 kHz. 

## Getting Started

Utilizing the [Wifi _Activity_Recognition repo](https://github.com/ermongroup/Wifi_Activity_Recognition) , the dataset can be downloaded [here](https://drive.google.com/file/d/19uH0_z1MBLtmMLh8L4BlNA0w-XAFKipM/view) . To preprocess the dataset, clone the [Wifi _Activity_Recognition repo](https://github.com/ermongroup/Wifi_Activity_Recognition) and run `python cross_vali_data_convert_merge.py` . The data is preprocessed by: 

- Resampaling signals from 1kHz to 500 Hz 
- Deleting no activity data

