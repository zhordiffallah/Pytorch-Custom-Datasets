# -*- coding: utf-8 -*-
"""TUT-SED2017-Dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kG0Ors92bWZJyOsRlngxpiLg0p-Jt9nC

## 🌏 **Building a Custom DataLoader in PyTorch for the TUT Sound Event Detection 2017 Dataset (TUT SED2017)**

### **Overview**
This notebook guides you through the process of creating a custom DataLoader in PyTorch specifically for the **TUT Sound Event Detection (SED) 2017** dataset. The goal is to efficiently load, process, and prepare this dataset for machine learning tasks, particularly for training and evaluating models that can classify environmental sounds based on audio data.

### **Objectives**
1. **Data Collection:**
   - Retrieve and organize sound event audio files from the TUT dataset.
   - Extract sound event labels for each audio file from the annotations provided.

2. **Custom DataLoader Creation:**
   - Implement a custom PyTorch `Dataset` class that handles the loading and preprocessing of the dataset.
   - Prepare the data for feeding into a deep learning model, ensuring that all necessary transformations are applied.

### **Structure**
The notebook is structured as follows:
1. **Data Preparation:** Gathering and merging all relevant data sources.
2. **DataLoader Implementation:** Writing the custom PyTorch `Dataset` class.
3. **DataLoader Usage:** Demonstrating how to use the custom DataLoader in a PyTorch training loop.
"""

# Import the drive module from google.colab to access Google Drive
# Mount the Google Drive to the Colab environment to access files and to download the dataset in your drive
# '/content/drive' is the directory where Google Drive will be mounted.
# After running this, you'll be prompted to authorize Colab to access your Drive.
from google.colab import drive
drive.mount('/content/drive')

"""### 📦 **Importing Necessary Libraries**

Here, we import essential libraries that will help us manipulate data, manage files, handle audio, and create custom datasets:

- **pandas**: For reading, processing, and analyzing data from files.
- **os**: To interact with the operating system, such as navigating directories and working with file paths.
- **glob**: Helps find pathnames that match specific patterns, which is useful for locating dataset files.
- **torch**: The core PyTorch library for tensor operations and deep learning models.
- **torchaudio**: A specialized PyTorch library for audio processing, essential for handling the TUT-SED 2017 dataset.
- **torch.utils.data.Dataset and DataLoader**: These utilities help us create and load custom datasets for model training.

"""

import pandas as pd
import os
import glob
import torch
import torchaudio
from torch.utils.data import Dataset, DataLoader

"""### 📦 **Downloading and Extracting the TUT-SED 2017 Dataset**
The **TUT-SED 2017** dataset is a comprehensive sound event detection (SED) dataset created for the **TUT Sound Events 2017** evaluation task. It contains environmental audio recordings that are annotated for sound events within the audio clips. The dataset is designed for training and testing algorithms to detect various sound events in realistic acoustic environments.

#### Key Features of the Dataset:
- **Audio Data**: The dataset consists of real-world audio recordings collected from an outdoor environment.
- **Duration**: Each audio clip is approximately 3 to 5 minutes long, recorded with a sampling rate of 44.1 kHz.
- **Annotations**: The dataset includes detailed annotations of sound event occurrences, specifying the type of sound and its temporal location within the audio clip.
- **Classes**: Common sound event categories include: brakes squeaking, car, children, large vehicle, people speaking, and people walking
- **Task**: The task associated with this dataset is to detect and label the occurrence of different sound events in a continuous audio stream.

#### Applications:
The TUT-SED 2017 dataset is primarily used for research in **sound event detection** and can be applied in various fields like:
- **Acoustic scene analysis**
- **Urban sound monitoring**
- **Audio-based surveillance**


More information and access to the dataset can be found on the official [Zenodo page](https://zenodo.org/record/400516).
To work with the **TUT-SED 2017** dataset, we first need to download it from Zenodo. Here's what's happening:

- **wget**: This command fetches the dataset as a `.zip` file from the provided URL. We rename the file to `tut-sed-2017-dataset.zip` for clarity.
- **unzip**: We extract the contents of the `.zip` file into a directory called `/content/dataset`.

This step ensures that all dataset files are available for use in the subsequent parts of our project.

"""

# Use wget to download the TUT-SED 2017 dataset from Zenodo using its URL
# The '-O' option renames the downloaded file as 'tut-sed-2017-dataset.zip'
!wget 'https://zenodo.org/api/records/400516/files-archive' -O tut-sed-2017-dataset.zip

# Unzipping the downloaded dataset file into a specified directory (/content/dataset)
# The '-d' option specifies the extraction directory
!unzip tut-sed-2017-dataset.zip -d /content/dataset

# Once the dataset is downloaded, it comes in multiple `.zip` files, each containing specific parts of the dataset, such as audio, metadata, and documentation.
# We will extract these files into corresponding directories for easy access:
# - **Metadata**: Unzips the **TUT-sound-events-2017-development.meta.zip** file, which contains the annotations for the dataset, into the `/content/dataset/meta` directory.
# - **Audio Part 1**: Unzips the first set of audio files, **TUT-sound-events-2017-development.audio.1.zip**, into `/content/dataset/audio1`.
# - **Audio Part 2**: Unzips the second set of audio files, **TUT-sound-events-2017-development.audio.2.zip**, into `/content/dataset/audio2`.
# - **Documentation**: Unzips the **TUT-sound-events-2017-development.doc.zip**, which contains the documentation for the dataset, into `/content/dataset/doc`.
!unzip /content/dataset/TUT-sound-events-2017-development.meta.zip -d /content/dataset/meta
!unzip /content/dataset/TUT-sound-events-2017-development.audio.1.zip -d /content/dataset/audio1
!unzip /content/dataset/TUT-sound-events-2017-development.audio.2.zip -d /content/dataset/audio2
!unzip /content/dataset/TUT-sound-events-2017-development.doc.zip -d /content/dataset/doc

# Check the contents of the audio1 folder
!ls /content/dataset/audio1/TUT-sound-events-2017-development/audio/street

# Check the contents of the audio2 folder
!ls /content/dataset/audio2/TUT-sound-events-2017-development/audio/street

# Check the contents of the meta folder
!ls /content/dataset/meta/TUT-sound-events-2017-development

# Display the contents of meta.txt
!cat /content/dataset/meta/TUT-sound-events-2017-development/meta.txt

"""### 🎶 **Merging Audio Files for Easier Access**

To simplify the process of accessing the audio files from the **TUT-SED 2017** dataset, we will merge the audio files from both parts (audio1 and audio2) into a single directory. This will make it easier to load and process all audio files in one place.

Here are the steps:

1. **Create a New Directory**: We create a new folder, `audio_merged`, where all the audio files will be consolidated.
2. **Move Audio Files**:
   - First, we move all audio files from **audio1** to the new `audio_merged` directory.
   - Then, we move the remaining files from **audio2** to the same `audio_merged` folder.

This step ensures that all audio files are organized in one place, facilitating seamless data loading and processing.


"""

# Create a new directory for merged audio files
!mkdir /content/dataset/audio_merged
# Move all files from audio1 to audio_merged
!mv /content/dataset/audio1/TUT-sound-events-2017-development/audio/street/* /content/dataset/audio_merged/
# Move all files from audio2 to audio_merged
!mv /content/dataset/audio2/TUT-sound-events-2017-development/audio/street/* /content/dataset/audio_merged/

# List the contents of the audio_merged folder
!ls /content/dataset/audio_merged
# Count the number of files in the audio_merged folder
!ls /content/dataset/audio_merged | wc -l

# Delete the audio1 and audio2 folders
!rm -r /content/dataset/audio1
!rm -r /content/dataset/audio2

"""### 🔄 **Loading and Preparing the Audio and Metadata**

Now, we need to load and organize both the audio files and the metadata for the TUT-SED 2017 dataset. Here's what we do:

1. **Retrieve Audio Files**: We use the `glob` library to gather all `.wav` audio files from the `audio_merged` folder. These files will be used for sound event detection.
  
2. **Load Annotations**: We load the metadata file (`meta.txt`), which contains important information like:
   - The path to the audio file.
   - The scene where the sound was recorded.
   - The onset and offset times of sound events.
   - The type of sound event (e.g., footsteps, speech, etc.).

   To make the data more readable, we define clear headers for each column. We also drop any unnecessary columns, like `Extra 1` and `Extra 2`.

This prepares both the audio and metadata for further processing.

"""

# Define headers for the columns in the sound event annotation file
# These columns correspond to the audio file path, scene label, onset time, offset time, and event label.
header = ["Audio file path", "Scene", "Onset", "Offset", "Event label", "Extra 1", "Extra 2"]

# Step 1: Retrieve all audio files from the merged audio directory using glob
# This step collects all .wav files from the specified directory, where the merged audio files are stored
audio_files = glob.glob('/content/dataset/audio_merged/*.wav')

# Step 2: Load the sound event annotations from the 'meta.txt' file located in the metadata folder
# The file is tab-delimited and contains information about sound events (e.g., start time, end time, and event label)
# Headers are added to improve interpretability of the loaded data
annotations = pd.read_csv('/content/dataset/meta/TUT-sound-events-2017-development/meta.txt', delimiter='\t', header=None, names=header)

# Remove unnecessary columns ('Extra 1' and 'Extra 2') from the annotations dataframe
annotations = annotations.drop(columns=['Extra 1', 'Extra 2'])

# Print the list of audio file paths
print("Audio Files:")
for audio_file in audio_files:
    print(audio_file)

# Print the first few rows of the annotations dataframe to see the loaded data
print("\nAnnotations:")
print(annotations.head())

# Save the DataFrame to a CSV file for future use
annotations.to_csv('processed_metadata.csv', index=False)
print("DataFrame has been saved to 'processed_data.csv'")

"""### 🛃 **CustomDataset Class**

The `CustomDataset` class is designed to facilitate working with audio data in PyTorch. It handles loading audio files and their corresponding labels, making it easier to integrate custom datasets into PyTorch's data loading pipeline.

- **Initialization (`__init__` method):**
  The class is initialized with:
  - The path to the directory containing audio files.
  - A CSV file containing labels for each audio file.
  - An optional transformation function to be applied to the audio data.

- **Dataset Length (`__len__` method):**
  This method returns the total number of samples in the dataset, which corresponds to the number of rows in the labels CSV file.

- **Fetching Items (`__getitem__` method):**
  Given an index, this method:
  - Retrieves the file path of the audio sample.
  - Loads the audio file using `torchaudio`.
  - Extracts the corresponding label from the labels DataFrame.
  - Returns a tuple containing the audio signal and its label.

- **Audio Path Retrieval (`get_audio_path` method):**
  Constructs and returns the full file path to an audio sample based on its index and the base directory where audio files are stored.

- **Label Retrieval (`get_audio_label` method):**
  Extracts and returns the label for a given audio sample based on its index in the labels DataFrame.

This class provides a structured way to manage and preprocess audio data for machine learning tasks using PyTorch.

"""

class CustomDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        """
        Initializes the CustomDataset.

        Parameters:
        - data (str): Directory path where audio files are stored.
        - labels (str): Path to the CSV file containing labels for the audio files.
        - transform (callable, optional): Optional transformation function to apply to the audio data.
        """
        self.data = data
        self.labels = pd.read_csv(labels)  # Load labels from the CSV file into a DataFrame
        self.transform = transform

    def __len__(self):
        """
        Returns the total number of samples in the dataset.

        Returns:
        - int: Number of samples, which is the length of the labels DataFrame.
        """
        return len(self.labels)

    def __getitem__(self, idx):
        """
        Retrieves an audio sample and its label based on the index.

        Parameters:
        - idx (int): Index of the sample to retrieve.

        Returns:
        - tuple: (signal, label) where `signal` is the loaded audio signal and `label` is the corresponding label.
        """
        audio_path = self.get_audio_path(idx)  # Get the file path for the audio sample
        label = self.get_audio_label(idx)      # Get the label for the audio sample
        signal, sr = torchaudio.load(audio_path)  # Load the audio file
        return signal, label

    def get_audio_path(self, idx):
        """
        Constructs the file path for an audio sample based on its index.

        Parameters:
        - idx (int): Index of the sample.

        Returns:
        - str: Full path to the audio file.
        """
        file_path = self.labels.iloc[idx, 0]  # Extract file path from the labels DataFrame
        file_name = file_path.split('/')[-1]
        path = os.path.join(self.data, file_name)  # Join directory path with filename from labels DataFrame
        return path

    def get_audio_label(self, idx):
        """
        Retrieves the label for a given audio sample based on its index.

        Parameters:
        - idx (int): Index of the sample.

        Returns:
        - str: Label for the audio sample.
        """
        label = self.labels.iloc[idx, 4]  # Extract label from the labels DataFrame at position 4
        return label

"""## 🧰 **Dataset usage**

In this section, we perform the following steps:

1. **Define Paths:**
   - Specify the directory where the audio files are stored.
   - Provide the path to the CSV file containing the annotations (labels) for these audio files.

2. **Initialize the Dataset:**
   - Create an instance of the `CustomDataset` class using the defined paths for audio data and annotations.

3. **Print Dataset Size:**
   - Output the total number of samples in the dataset. This helps verify that the dataset is loaded correctly and provides insight into its size.

This process ensures that the dataset is properly set up and gives a clear understanding of the amount of data available for analysis or model training.

"""

# Define the path to the directory containing audio files
audio_data_path = '/content/dataset/audio_merged'

# Define the path to the CSV file containing annotations (labels) for the audio files
annotations_path = '/content/dataset/meta/TUT-sound-events-2017-development/processed_metadata.csv'

# Create an instance of the CustomDataset class with the specified paths
tutsed2017dataset = CustomDataset(audio_data_path, annotations_path)

# Print the total number of samples in the dataset
print(f"There are {len(tutsed2017dataset)} samples in the dataset")

"""## ⌨ **Accessing and Inspecting a Dataset Sample**

In this section, we perform the following steps to inspect a sample from the dataset:

1. **Retrieve a Sample:**
   - We access the first sample from the dataset using `ICBHI[0]`. This retrieves a tuple consisting of the audio signal and its corresponding label.

2. **Inspect Signal and Label:**
   - We then print the shape of the audio signal and the label associated with this sample. This helps us understand the structure of the audio data (e.g., its dimensions) and verify the label information.

By examining a sample, we gain insights into the format of the audio data and the type of labels provided, which is crucial for ensuring data consistency and preparing for further analysis or model training.

"""

# Retrieve the first sample from the dataset
signal, label = tutsed2017dataset[1]

# Print the shape of the audio signal and the corresponding label
signal, label

"""## 👏 **Conclusion**
By completing these steps, we’ve established a solid foundation for working with the TUTSED sound dataset. This preparation is crucial for subsequent stages such as data preprocessing, feature extraction, and model training. With the dataset correctly set up and verified, we can now proceed to further analysis and experimentation to advance our research or project objectives. Feel free to build on this setup with additional analysis, feature extraction, or model training as needed.
"""