# CAT_DSR
This is the code of the paper: **Convolution-Augmented Transformers for Enhanced Speaker-Independent Dysarthric Speech Recognition**

We modified and adapted the Conformer Small architecture available in the [Speechbrain](https://github.com/speechbrain/speechbrain) toolkit. 

For more implementation details of our system, please refer to our paper. 

## Quick Start
To get started, please follow these simple steps to install SpeechBrain first. 

### install via PyPI
1. Install SpeechBrain using PyPI:

```python
pip install speechbrain
```
2. Access SpeechBrain in the python code:
```python
import speechbrain as sb
```

### Paper reproduction
![Methodology Overview](https://github.com/user-attachments/assets/777c5bb5-3c15-4fc7-8770-fb33a81473b6)

#### Data configuration
1. Download [UASPEECH](https://ieee-dataport.org/documents/uaspeech) dataset & [TORGO](https://www.cs.toronto.edu/~complingweb/data/TORGO/torgo.html) dataset.
2. Refer to the "EXPERIMENTS" section of our paper to partition the data and configure metadata(*.csv) according to [Speechbrain](https://github.com/speechbrain/speechbrain) format. Or you can look up for appropriate partition csv files from folder ```Partitions```.

#### Training SI Dysarthric Speech Recognition (DSR) model
1. Modify the csv files in ```Partitions``` to adjust the audio path to your data storage
2. Modify the parameters in the ```recipes/hparams/conformer_small.yaml``` configuration file, especially ```output_folder```, ```data_folder```, ```train_csv```, ```valid_csv```, ```test_csv```, ```number_of_epochs```, ```freeze_num_encoder_layers``` and ```freeze_num_decoder_layers```. We also provided example of P3 to showcase how we configure the training. 
3. Training instructions:
```python
cd recipes
python train.py hparams/conformer_small.yaml
```
The results will be saved in the ```output_folder``` specified in the YAML file

if you want to run it on the **test sets** only, you can add the flag --test_only to the following comman:
```python
python train.py hparams/conformer_small.yaml --test_only
```
##### Training Pipeline
![transfer_learning_pipelines](https://github.com/user-attachments/assets/0bd7e6bd-07b5-4d79-a926-534acf90b80e)
*  Pipeline 1 (P1): The base model was fine-tuned on UA-Speech control data and then TORGO control data, resulting in Control 1.
*  Pipeline 2 (P2): The base model was fine-tuned on TORGO control and then UA-Speech control, resulting in Control 2.
*  Pipeline 3 (P3): The base model was fine-tuned on the combined control data from both UA-Speech and TORGO to create Control 3.
*  Pipeline 4 (P4): The base model was fine-tuned on the UA-Speech control to create Control 4.
*  Pipeline 5 (P5): The base model was fine-tuned on the TORGO control data to build Control 5.

##### Cross-Dataset Validation 
We tested the model performance by conducting **cross-dataset validation**.
1. SI dysarthric models trained on UASPEECH were tested on TORGO dataset's isolated speech and continuous speech seperately
2. SI dysarthric models trained on TROGO were tested on entire UASPEECH.

Specific paritition can be found under ```Partitions/test/UASPEECH_dysarthric_test``` & ```Partitions/test/TORGO_dysarthric_test```

## Acknowledgement
This work is based on the [Speechbrain](https://github.com/speechbrain/speechbrain) toolkit and we have modifed the original repository to better fit our task based on Conformer_Small. In addition, we would like thank the effort of researcher of UASPEECH and TORGO dataset. 
