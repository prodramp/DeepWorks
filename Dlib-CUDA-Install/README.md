# Dlib CUDA Install # 

This video is all you need to install DLib with Nvidia CUDA and cudNN support in your Python 3.x installation created using Conda. You will also learn fixing the problem specific to following error:


ImportError: /home/avkash/anaconda3/envs/dw39/lib/python3.9/site-packages/zmq/backend/cython/../../../../.././libstdc++.so.6: version `GLIBCXX_3.4.29' not found (required by /home/avkash/.cache/torch_extensions/py39_cu113/fused/fused.so)

<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp;Dev Tools:&nbsp; Installing dlib with Nvidia Cuda & cudnn on Ubuntu 22.04  with Python and Conda</b></td>
    </tr>
    <tr>
        <td>
            <div>                

[![Installing dlib with Nvidia Cuda & cudnn on Ubuntu 22.04  with Python and Conda](https://img.youtube.com/vi/6OTrrB6tTEo/0.jpg)](https://www.youtube.com/watch?v=6OTrrB6tTEo)

</tr>
</table>


This video covers the following:
0. Ubuntu 22.04 with latest Kernel
1. dlib (latest from GitHub)
2. Cuda Toolkit 11.7 and cuDNN 8.4 Install
3. Python 3.9 with Conda 
4. Torch, TensorFlow and JAX with GPU Support

dlib GitHub:
- https://github.com/davisking/dlib

## Commands Used on this Tutorials

- $ sudo apt-get update
- $ sudo apt-get -y install librust-dlib-dev
- $ sudo apt-get install libx11-dev

## Cloning and installing dlib GitHub Repo
- $ git clone https://github.com/davisking/dlib.git
- $ mkdir build
- $ cd build
- $ cmake .. ; cmake --build . --config Release
- $ sudo ldconfig
- $ cd ..

Note: Use pkg-config to provide path to Dlib’s include directory and link Dlib library file.

- pkg-config --libs --cflags dlib-1
- Note: Install pkg-config using apt or apt-get if you don't have

## Installaing dlib with Python environment
- conda activate -your-python-environment-name
- $ pip install --upgrade dlib (Optional)
- $ cd dlib (Please make sure you are inside the dlib root folder and have access to setup.py)
- $ python setup.py install


## Removing dlib from python environment
- $ rm -rf dist
- $ rm -rf tools/python/build
- $ rm python_examples/dlib.so

## Install jupyter lab for your conda based Python environment:
- $ conda install -c conda-forge jupyterlab
