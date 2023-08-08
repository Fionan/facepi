# FacePi - Face Recognition and Comparison Tool

FacePi is a collection of Python scripts that utilize libraries like OpenCV, dlib, and ffmpeg to process screenshots from videos, detect faces, and compare them against a predefined list of known faces.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Target Audience](#target-audience)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

FacePi is designed to streamline the process of face recognition and comparison using various tools and libraries. It's particularly useful for developers, students, or anyone interested in exploring face matching techniques.

## Features

- Capture screenshots from videos using ffmpeg.
- Utilize OpenCV and dlib to detect faces in screenshots.
- Compare detected faces against a known list of faces.
- Flexible command-line interface for easy integration.

## Target Audience

FacePi is suitable for:

- Developers who want to experiment with face recognition algorithms.
- Students exploring computer vision and facial analysis.
- Individuals interested in understanding face matching techniques.

## Prerequisites

Before using FacePi, ensure you have the following prerequisites:

- [ffmpeg](https://ffmpeg.org/) (for capturing video frames)
- Python (tested with version 3.11.3)
- Additional prerequisites...
(TO-DO)

## Installation

To set up FacePi, follow these steps:

1. Clone this repository.
2. Install the required Python dependencies using the following command:

   ```bash
   pip install -r requirements.txt

## Usage
To use FacePi, follow these steps:

prerequisite:
Configure your list of known faces known_faces/<namedface>/<images-of-namedface>

Capture screenshots from your video using ffmpeg using 1_extract_frames.py

```python
        python .\1_extract_frames.py .\<video-folder>\            
```

Run the FacePi script 2_find_faces.py and options:

```python
        # find faces in images folder outputting to a particular folder
        python .\2_find_faces.py ./<images-input-folder> ./<output-folder>   
```

Compare against known faces using 3_list_known_faces.py

```python
        # run list known faces script specifying the faces folder the known faces and run a report
        python ./3_list_known_faces.py -f <faces-folder> -k <known-faces-folder> -r
```


## Licence
(TO-DO)