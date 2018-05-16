# DnCNN-tensorflow
[DnCNN](http://www4.comp.polyu.edu.hk/~cslzhang/paper/DnCNN.pdf) implement based on tensorflow-1.8
# [Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising](http://ieeexplore.ieee.org/document/7839189/)
# To run this code
- Python3 with dependencies:
		scipy
		numpy
		tensorflow-gpu
		scikit-image
		pillow
		h5py

# Generating training data
- 'generate_data.py'. You may need to modify the path to trainning datasets. According to the [MatConvNet code](https://github.com/cszn/DnCNN) offered by authors, there are some blank(zero) data in the generated training dataset.

# Trainning
- [train] 'train_DnCNN.py'

# Testing
- [test] 'Validate_DnCNN.py' You need to change the path and filetype of your testset. While I generated the testset by matlab to make faire when competing with other methods.

# Results
- Only denoising methods were focused in my work.

## Gaussian Denoising

**The average PSNR(dB) results of different methods on the BSD68 dataset.**

|  Noise Level | BM3D | WNNM  | EPLL | MLP |  CSF |TNRD  | DnCNN-S | DnCNN-B | DnCNN-S-Re |
|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| 15  |  31.07  |   31.37   | 31.21  |   -   |  31.24 |  31.42 | 31.73 | 31.61  |  -  |
| 25  |  28.57  |   28.83   | 28.68  | 28.96 |  28.74 |  28.92 | **29.23** | 29.16  | -  |
| 50  |  25.62  |   25.87   | 25.67  | 26.03 |    -   |  25.97 | **26.23** | **26.23**  | - |

**The average PSNR(dB) results of different methods on the Set12 dataset.**

|  Noise Level | BM3D | WNNM  | EPLL | MLP |  CSF |TNRD  | DnCNN-S | DnCNN-B | DnCNN-S-Re |
|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| 15  |  32.372  |   32.696   | 32.138  |   -   |  32.318 |  32.502 | 32.859 | 32.680  |  -  |
| 25  |  29.969  |   30.257   | 29.692  | 30.027 |  29.837 |  30.055 | 30.436 | 30.362  | 30.33  |
| 50  |  26.722  |   27.052   | 26.471  | 26.783 |    -   |  26.812 | 27.178 | 27.206  | - |