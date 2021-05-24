# Sleep-EDF Dataset

**Source:** [ Physionet ](https://www.physionet.org/content/sleep-edfx/1.0.0/ )

**Task:** Classification of sleep stages based on raw single channel EEGs

**Number of instances:**

**Number of attributes:** 2

This dataset contains 197 whole-night PolySomnoGraphic sleep recordings. The construct the samples by duplicating minority sleep stages to create a class balance training set, where all sleep stages have the same number of samples. 

**Cite:** 

```
@article{gold2000physio,
  title={PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals},
  author={Goldberger, A. and Amaral, L. and Glass, L. and Hausdorff, J. and Ivanov, P. C. and Mark, R. and Mietus, Joseph E. and Moody, George B and Peng, Chung Kang and Stanley, H Eugene},
  journal={Circulation},
  volume={1},
  number={23},
  pages={e215–e220},
  year={2000},
  publisher={Lippincott Williams & Wilkins},
}
```

## Getting started

Using the [deepsleepnet repo](https://github.com/akaraspt/deepsleepnet) , the dataset can be downloaded by running `download_physionet.sh` . This scripts downloads the dataset directly from the source, [ Physionet ](https://www.physionet.org/content/sleep-edfx/1.0.0/ ). To preprocess the dataset, run  `python preparephysionet.py` , which 

- Merges the N3 and N4 stages into a single stage 
- Only includes data from 30 minutes before and after sleep periods, as the task is only concerned with classifiying sleep stages. 
- Removes unknown and movement labels from the dataset

There is no preprocessing done to the Fpz-Cz and Pz-Cz channels. 

