# PyTorch Custom Datasets for public sound corpora

This repository contains custom PyTorch `Dataset` classes for various sound datasets. The goal is to provide an easy-to-use interface for loading, preprocessing, and managing audio datasets in a structured way using the PyTorch framework.

## 📁 Datasets

This repository includes custom datasets for:

- **ICBHI Respiratory Sound Database (The Respiratory Sound database - ICBHI 2017 Challenge)** : The database consists of a total of 5.5 hours of recordings containing 6898 respiratory cycles, of which 1864 contain crackles, 886 contain wheezes, and 506 contain both crackles and wheezes, in 920 annotated audio samples from 126 subjects. The cycles were annotated by respiratory experts as including crackles, wheezes, a combination of them, or no adventitious respiratory sounds. The recordings were collected using heterogeneous equipment and their duration ranged from 10s to 90s.
- **TUT Sound Events 2017** : Introduced by Annamaria Mesaros et al. in [TUT database for acoustic scene classification and sound event detection](https://ieeexplore.ieee.org/document/7760424/), the TUT Sound Events 2017 dataset contains 24 audio recordings in a street environment and contains 6 different classes. These classes are: brakes squeaking, car, children, large vehicle, people speaking, and people walking.


## ⚙️ Installation

To use the custom datasets, first clone this repository:

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/zhordiffallah/Pytorch-Custom-Datasets.git)
```
Navigate to the cloned directory:

```bash
cd Pytorch-Custom-Datasets
```
Once you have cloned the repository and installed the necessary dependencies, you can use any of the available datasets in your PyTorch projects. Below is an example of how to use a custom dataset:

```bash
from your_dataset_module import CustomDataset
from torch.utils.data import DataLoader
# Initialize the dataset
dataset = CustomDataset('path/to/your/audio/files', 'path/to/your/annotations')
# Create a DataLoader
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```
## 🚀 Contributing
Contributions are welcome! Feel free to submit a pull request if you want to add a new dataset or improve the repository.
