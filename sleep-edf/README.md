# Sleep-EDF Dataset

**Source:** [ Physionet ](https://www.physionet.org/content/sleep-edfx/1.0.0/ )

**Task:** Classification of sleep stages based on raw single channel EEGs

**Number of instances:**

**Number of attributes:**

This dataset contains 197 whole-night PolySomnoGraphic sleep recordings. The construct the samples by duplicating minority sleep stages to create a class balance training set, where all sleep stages have the same number of samples. 

**Cite:** 

```
Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.
```

## Getting started

Using the [deepsleepnet repo](https://github.com/akaraspt/deepsleepnet) , the dataset can be downloaded by running `download_physionet.sh` . This scripts downloads the dataset directly from the source, [ Physionet ](https://www.physionet.org/content/sleep-edfx/1.0.0/ ). To preprocess the dataset, run  `python preparephysionet.py` , which 

- Merges the N3 and N4 stages into a single stage 
- Only includes data from 30 minutes before and after sleep periods, as the task is only concerned with classifiying sleep stages. 
- Removes unknown and movement labels from the dataset

There is no preprocessing done to the Fpz-Cz and Pz-Cz channels. 

