# PyTorch Custom Datasets for public sound corpora

This repository contains custom PyTorch `Dataset` classes for various sound datasets. The goal is to provide an easy-to-use interface for loading, preprocessing, and managing audio datasets in a structured way using the PyTorch framework.

## 📁 Datasets

This repository includes custom datasets for:

- **Sound Event Detection Datasets**
- **Biomedical Sound Datasets**


## ⚙️ Installation

To use the custom datasets, first clone this repository:

```bash
git clone https://github.com/your-username/your-repo-name.git

Navigate to the cloned directory:

```bash
cd your-repo-name

Once you have cloned the repository and installed the necessary dependencies, you can use any of the available datasets in your PyTorch projects. Below is an example of how to use a custom dataset:

```bash
from your_dataset_module import CustomDataset
from torch.utils.data import DataLoader
# Initialize the dataset
dataset = CustomDataset('path/to/your/audio/files', 'path/to/your/annotations')
# Create a DataLoader
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

## Contributing
Contributions are welcome! Feel free to submit a pull request if you want to add a new dataset or improve the repository.
