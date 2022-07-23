# Diffusion Model - Hands on Exercise #

Diffusion models have seen wide success in image generation. Autoregressive models, GANs, VQ-VAE Transformer based methods have all made remarkable progress in text-to-image research. More recently, Diffusion models have been explored for text-to-image generation, including the concurrent work of DALL-E 2.


## Denoising Diffusion Model Test and Training

- https://github.com/hmdolatabadi/denoising_diffusion
- Download the model checkpoint from here
  - https://drive.google.com/drive/folders/1R8xmSjLSM1vXWpvZrv3mPE52ImCjVzxK

```
Training the model

$ python diffusion_lightning.py --train \
    --config config.json \
    --ckpt_dir PATH_TO_CHECKPOINTS \
    --ckpt_freq CHECKPOINT_FREQ \
    --n_gpu NUM_AVAIL_GPUS

Testing the model to show diffusion results:

$ python diffusion_lightning.py \
    --config config.json \
    --model_dir MODEL_DIRECTORY \
    --sample_dir PATH_TO_SAVE_SAMPLES \
    --n_samples NUM_SAMPLES

To change the image resolution, please ownload the diffusion_cifar10_new.json to local machine, edit it to set resolution to 256 or desired number from 32 and then re-upload it back to your /content/denoising_diffusion/config/ folder.

"dataset": {
    "name": "cifar10",
    "path": "/cifar10_data/",
    "resolution": 256 
}

```

## Orignal Implementations
- Original with Research Paper
- https://hojonathanho.github.io/diffusion/ (TensorFlow Implementation)
    - https://github.com/hojonathanho/diffusion

## Other Implementations 
- https://github.com/hmdolatabadi/denoising_diffusion (Torch-lightening Implementation)
- https://github.com/acids-ircam/diffusion_models (Torch-lightening + JAX Implementation)
- https://github.com/lucidrains/denoising-diffusion-pytorch (PyTorch Implementation)
- https://github.com/rosinality/denoising-diffusion-pytorch (PyTorch Implementation)
- https://github.com/ermongroup/ddim (PyTorch Implementation)
- https://github.com/pesser/pytorch_diffusion (PyTorch Implementation)
- https://github.com/awjuliani/pytorch-diffusion (PyTorch Implementation)
- https://github.com/w86763777/pytorch-ddpm (PyTorch Implementation)

## Awesome Diffusion Models
- https://github.com/heejkoo/Awesome-Diffusion-Models

## Articles
- https://cascaded-diffusion.github.io/ (Cascade Diffusion - Google Imagen)
- https://hmdolatabadi.github.io/posts/2020/09/ddp/ 
- https://towardsdatascience.com/diffusion-models-made-easy-8414298ce4da

### Video Diffusion
- https://video-diffusion.github.io/
  - https://github.com/lucidrains/video-diffusion-pytorch

## Research Papers 
- https://arxiv.org/abs/2006.11239
- https://arxiv.org/abs/1503.03585
- https://arxiv.org/abs/1907.05600
