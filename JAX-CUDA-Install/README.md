# JAX and JAXlib installation with CUDA and cudNN # 

This video is all you need to install JAX with Nvidia CUDA and cudNN support in your Python 3.x installation. This video covers the following:

1. Python 3.9
2. [JAX with JAXLib 0.3.14](https://github.com/google/jax)
3. Cuda Toolkit 11.7
4. cuDNN 8.4 Installation
5. Conda Toolkit 11.7
6. Torch, TensorFlow and JAX with GPU Support

Resources:
- [jax and jaxlib]
- 

<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp;YouTube Video:&nbsp;JAX installation with Nvidia CUDA and cudNN support (Fixing most common installation error)</b></td>
    </tr>
    <tr>
        <td>
            <div>
                
[![JAX installation with Nvidia CUDA and cudNN support (Fixing most common installation error)](https://img.youtube.com/vi/auksaSl8jlM/0.jpg)](https://www.youtube.com/watch?v=auksaSl8jlM)

  </tr>
</table>


## Checking cudNN nn my machine

```
$ cat /usr/local/cuda-11.7/include/cudnn_version.h

 #ifndef CUDNN_VERSION_H_
 #define CUDNN_VERSION_H_

 #define CUDNN_MAJOR 8
 #define CUDNN_MINOR 4
 #define CUDNN_PATCHLEVEL 1

 #define CUDNN_VERSION (CUDNN_MAJOR * 1000 + CUDNN_MINOR * 100 + CUDNN_PATCHLEVEL)
```

## Checking cuda version in my machine

```
$ nvidia-smi

Mon Jul  4 12:25:56 2022       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 515.57       Driver Version: 515.57       CUDA Version: 11.7     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA TITAN Xp     Off  | 00000000:02:00.0  On |                  N/A |
| 23%   32C    P8    18W / 250W |    412MiB / 12288MiB |     13%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      2008      G   /usr/lib/xorg/Xorg                104MiB |
|    0   N/A  N/A      2170      G   /usr/bin/gnome-shell               82MiB |
|    0   N/A  N/A      4777      G   ...457980903654285300,131072       73MiB |
|    0   N/A  N/A      7536      C   python                            147MiB |
+-----------------------------------------------------------------------------+
```

## Uninstalling JAX and JAXlib completely

Make sure to install at the from Conda root and any Conda environment

- pip uninstall jax
- pip uninstall jaxlib


## Validating JAX and JAXlib Uninstallation

Checking that both jax and jaxlib are not available

```
(base) avkash@DeepWorks:~$ pip show jax
WARNING: Package(s) not found: jax
(base) avkash@DeepWorks:~$ pip show jaxlib
WARNING: Package(s) not found: jaxlib

(base) avkash@DeepWorks:~$ conda activate dl39
(dl39) avkash@DeepWorks:~$ pip show jaxlib
WARNING: Package(s) not found: jaxlib
(dl39) avkash@DeepWorks:~$ pip show jax
WARNING: Package(s) not found: jax

(dl39) avkash@DeepWorks:~$ python
Python 3.9.12 (main, Jun  1 2022, 11:38:51) 
[GCC 7.5.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import jax
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'jax'
>>> import jaxlib
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'jaxlib'
>>> quit()

```

## Selecting correct JAX package for CUDA and cudNN

Note: [DO NOT USE]
- https://storage.googleapis.com/jax-releases/jax_releases.html

[USE FOLLOWING FOR jax with GPU]
- https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

- cuda11/jaxlib-0.3.14+cuda11.cudnn805-cp310-none-manylinux2014_x86_64.whl
- cuda11/jaxlib-0.3.14+cuda11.cudnn805-cp37-none-manylinux2014_x86_64.whl
- cuda11/jaxlib-0.3.14+cuda11.cudnn805-cp38-none-manylinux2014_x86_64.whl
- cuda11/jaxlib-0.3.14+cuda11.cudnn805-cp39-none-manylinux2014_x86_64.whl
- cuda11/jaxlib-0.3.14+cuda11.cudnn82-cp310-none-manylinux2014_x86_64.whl
- cuda11/jaxlib-0.3.14+cuda11.cudnn82-cp37-none-manylinux2014_x86_64.whl
- cuda11/jaxlib-0.3.14+cuda11.cudnn82-cp38-none-manylinux2014_x86_64.whl
- cuda11/jaxlib-0.3.14+cuda11.cudnn82-cp39-none-manylinux2014_x86_64.whl

## JAX and JAXlib Installation 

### Command

pip install --upgrade jax==0.3.14 jaxlib==0.3.14+cuda11.cudnn805 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

```
Looking in links: https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
Collecting jax==0.3.14
  Using cached jax-0.3.14-py3-none-any.whl
Collecting jaxlib==0.3.14+cuda11.cudnn805
  Using cached https://storage.googleapis.com/jax-releases/cuda11/jaxlib-0.3.14%2Bcuda11.cudnn805-cp39-none-manylinux2014_x86_64.whl (249.7 MB)
Requirement already satisfied: typing-extensions in ./anaconda3/envs/dl39/lib/python3.9/site-packages (from jax==0.3.14) (4.2.0)
Requirement already satisfied: absl-py in ./anaconda3/envs/dl39/lib/python3.9/site-packages (from jax==0.3.14) (1.1.0)
Requirement already satisfied: opt-einsum in ./anaconda3/envs/dl39/lib/python3.9/site-packages (from jax==0.3.14) (3.3.0)
Requirement already satisfied: scipy>=1.5 in ./anaconda3/envs/dl39/lib/python3.9/site-packages (from jax==0.3.14) (1.8.1)
Requirement already satisfied: numpy>=1.19 in ./anaconda3/envs/dl39/lib/python3.9/site-packages (from jax==0.3.14) (1.23.0)
Requirement already satisfied: etils[epath] in ./anaconda3/envs/dl39/lib/python3.9/site-packages (from jax==0.3.14) (0.6.0)
Requirement already satisfied: flatbuffers<3.0,>=1.12 in ./anaconda3/envs/dl39/lib/python3.9/site-packages (from jaxlib==0.3.14+cuda11.cudnn805) (1.12)
Requirement already satisfied: zipp in ./anaconda3/envs/dl39/lib/python3.9/site-packages (from etils[epath]->jax==0.3.14) (3.8.0)
Requirement already satisfied: importlib_resources in ./anaconda3/envs/dl39/lib/python3.9/site-packages (from etils[epath]->jax==0.3.14) (5.8.0)
Installing collected packages: jaxlib, jax
Successfully installed jax-0.3.14 jaxlib-0.3.14+cuda11.cudnn805
```

## Installation Validation 

```
(dl39) avkash@DeepWorks:~$ python
Python 3.9.12 (main, Jun  1 2022, 11:38:51) 
[GCC 7.5.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import jaxlib
>>> jaxlib.__version__
'0.3.14'
>>> import jax
>>> jax.__version__
'0.3.14'
>>> jax.devices()
[GpuDevice(id=0, process_index=0)]
>>> import torch; print(torch.cuda.is_available())
True
>>> import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
>>> 
```