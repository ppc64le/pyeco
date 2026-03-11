## ✅ Program : Torch / TorchVision / TorchAudio Validation Scripts
### Purpose:
Provides lightweight, network‑free test scripts to verify that torch, torchvision, and torchaudio are installed correctly and functioning without triggering known issues like the torchvision::nms registration conflict.

### Packages used:
torch
torchvision
torchaudio

### Functionality:
`torchvision_example.py`

Safe import of torchvision
Skips automatically if NMS conflict appears
Runs basic transforms + FakeData + small CNN (NMS‑free)

`torchaudio_example.py`

Generates sine wave
Resamples audio
Computes Spectrogram / MelSpectrogram / MFCC
Runs small Conv1d model on MFCC features

`sub-test1.py`

PIL + Tensor transforms
Optional transforms.v2
FakeData (grayscale)
Saves image grid using torchvision.utils

`sub-test2.py`

resnet18(weights=None) forward test
torchvision.transforms.functional operations
AutoAugment and interpolation tests

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```
