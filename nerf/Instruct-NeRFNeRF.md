# Instruct-NeRF2NeRF - Editing 3D Scenes with Instructions

Instruct-NeRF2NeRF enables instruction-based editing of NeRFs via a 2D diffusion model

## Overview
We propose a method for editing NeRF scenes with text-instructions. Given a NeRF of a scene and the collection of images used to reconstruct it, our method uses an image-conditioned diffusion model (InstructPix2Pix) to iteratively edit the input images while optimizing the underlying scene, resulting in an optimized 3D scene that respects the edit instruction. We demonstrate that our proposed method is able to edit large-scale, real-world scenes, and is able to accomplish more realistic, targeted edits than prior work.

## How it works
Our method gradually updates a reconstructed NeRF scene by iteratively updating the dataset images while training the NeRF:

- An image is rendered from the scene at a training viewpoint.
- It is edited by InstructPix2Pix given a global text instruction.
- The training dataset image is replaced with the edited image.
- The NeRF continues training as usual.

<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp; Instruct-NeRF2NeRF - Combining Diffusion Models with NeRF to create new NeRF Objects</b></td>
    </tr>
    <tr>
        <td>
            <div>
                
[![Instruct-NeRF2NeRF - Combining Diffusion Models with NeRF to create new NeRF Objects](https://img.youtube.com/vi/XAZJuY2Gb0Y/0.jpg)](https://www.youtube.com/watch?v=XAZJuY2Gb0Y)

  </tr>
</table>

<video src="https://github.com/prodramp/DeepWorks/blob/main/videos/face.mp4" controls="controls" style="max-width: 730px;"></video>
  

## Project URL
- https://instruct-nerf2nerf.github.io/

## Source Code
- Not Available (as of April 5th 2023)

## Resources 
- https://instruct-nerf2nerf.github.io
- https://github.com/nerfstudio-project/nerfstudio
- https://www.timothybrooks.com/instruct-pix2pix
- https://github.com/timothybrooks/instruct-pix2pix
