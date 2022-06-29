# Instant NeRF: Instant Neural Graphics Primitives (Nvidia Research) # 

The new NVIDIA NGP Instant NeRF is a great introduction to getting started with neural radiance fields. 
With your own video and/or image dataset, you can compile the codebase, prepare your images, and train your first NeRF.
Unlike other NeRF implementations, Instant NeRF only takes a few minutes to train a great-looking visual. This video is all you need to convert a video or image to NeRF scenes on Ubuntu. 

<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp;YouTube Video:&nbsp;NeRF: Create and play with your own NeRF scene from a video or image (Full Hands-on Tutorial) </b></td>
    </tr>
    <tr>
        <td>
            <div>
                
[![NeRF: Create and play with your own NeRF scene from a video or image (Full Hands-on Tutorial)](https://img.youtube.com/vi/Yejdb9l1w2Q/0.jpg)](https://www.youtube.com/watch?v=Yejdb9l1w2Q)

  </tr>
</table>

<div align="center">
  <img src="https://github.com/prodramp/DeepWorks/blob/main/Instant-NGP/images/nerf.png?raw=true" width="1000" />
</div> 

### Your build environment must have the following:
- Re-install CUDA Toolkit (1.17) latest with nvcc match with same toolkit (1.17) version 
- Install Python 3.9. If you are new to Python, this is not the latest version.
- Use CMake 3.22 and make sure that Python 3.9 is used to compile the codebase.
- Make sure G++ and gcc are latest and ffmpeg, colmap, qt packages are install


## Download and Build Library
Begin by cloning this repository and all its submodules using the following command:
```
$ git clone --recursive https://github.com/nvlabs/instant-ngp
$ cd instant-ngp
```

Building instant-ngp Library

```
instant-ngp$ cmake . -B build
instant-ngp$ cmake --build build --config RelWithDebInfo -j 16
```

### Package must be installed in machine to build instant-ngp library
- Python 3.9 with the following packages
  - colmap, opencv-python, opencv-python-headless, pyside6, pyqt6
- Ubuntu 22.02 must have the following library:
  - ffmpeg
  - colmap
  - qt5

### Commands for various operations
```
$ python scripts/colmap2nerf.py --video_in ~/Downloads/3dobj.mp4 --video_fps 10 --run_colmap --aabb_scale 4
$ python scripts/colmap2nerf.py --video_in ~/Downloads/aashil.mp4 --video_fps 5 --run_colmap --aabb_scale 4
$ python scripts/colmap2nerf.py --video_in ~/Downloads/avkash.mp4 --video_fps 5 --run_colmap --aabb_scale 4
$ python scripts/colmap2nerf.py --video_in ~/work/ngp-work/jcb/jcb.mp4 --video_fps 2 --run_colmap --aabb_scale 4 --out ~/work/ngp-work/jcb/transforms.json
$ python scripts/convert_image.py --input ~/work/ngp-work/gigapixel/tokyo-12gb.jpg  --output ~/work/ngp-work/gigapixel/tokyo_12gb.bin
$ ./build/testbed --scene ~/work/ngp-work/gigapixel/tokyo_10mb.bin
```

### Research Paper and Code 
- [Research Paper](https://nvlabs.github.io/instant-ngp/assets/mueller2022instant.pdf)
- [Introduction video](https://nvlabs.github.io/instant-ngp/assets/mueller2022instant.mp4)
- [Instant-ngp GitHub Source Code](https://github.com/NVlabs/instant-ngp)
- [NeRF Datasets](https://github.com/nickponline/dd-nerf-dataset)

### Resources & Articles ###
- https://www.matthewtancik.com/nerf
- https://www.matthewtancik.com/learnit
- https://pratulsrinivasan.github.io/nerv/
- https://developer.nvidia.com/blog/getting-started-with-nvidia-instant-nerfs/
