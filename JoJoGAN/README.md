# JoJoGAN: OneShot Face Stylization  # 

<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp;Part 1/3:&nbsp; One-shot Face Stylization with JoJoGAN - In-depth face style transfer tutorial</b></td>
    </tr>
    <tr>
        <td>
            <div>                

[![One-shot Face Stylization with JoJoGAN - In-depth face style transfer tutorial - Part (1/3)](https://img.youtube.com/vi/uXBbY1_vhSQ/0.jpg)](https://www.youtube.com/watch?v=uXBbY1_vhSQ)

</tr>
</table>

<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp;Part 2/3:&nbsp; One-shot Face Stylization with JoJoGAN - Code Walkthrough with Explanations - Part (2/3)</b></td>
    </tr>
    <tr>
        <td>
            <div>                

[![One-shot Face Stylization with JoJoGAN - Code Walkthrough with Explanations - Part (2/3)](https://img.youtube.com/vi/K1qPbjrJuKA/0.jpg)](https://www.youtube.com/watch?v=K1qPbjrJuKA)

</tr>
</table>

<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp;Part 3/3:&nbsp; One-shot Face Stylization with JoJoGAN - Model Save, Export and Deployment</b></td>
    </tr>
    <tr>
        <td>
            <div>                

[![One-shot Face Stylization with JoJoGAN - Model Save, Export and Deployment - Part (3/3)](https://img.youtube.com/vi/lMl7Yd7jC6A/0.jpg)](https://www.youtube.com/watch?v=lMl7Yd7jC6A)

</tr>
</table>

### Why JoJoGAN
- JoJoGAN needs just one reference and as little as 30 seconds of training time. 
- JoJoGAN can use extreme style references (say, animal faces) successfully. Furthermore, one can control what aspects of the style are used and how much of the style is applied. 
- Qualitative and quantitative evaluation show that JoJoGAN produces high quality high resolution images that vastly outperform the current state-of-the-art.

### How to works:
- A style mapper applies some fixed style to its input images (so, for example, taking faces to cartoons). 
- This paper describes a simple procedure -- JoJoGAN -- to learn a style mapper from a single example of the style. 
- JoJoGAN uses a GAN inversion procedure and StyleGAN's style-mixing property to produce a substantial paired dataset from a single example style.
- The paired dataset is then used to fine-tune a StyleGAN. An image can then be style mapped by GAN-inversion followed by the fine-tuned StyleGAN. 

<div align="center">
  <img src="https://github.com/prodramp/DeepWorks/blob/main/JoJoGAN/images/jojo01.png?raw=true" width="800" />
</div> 
<div align="center">
  <img src="https://github.com/prodramp/DeepWorks/blob/main/JoJoGAN/images/jojo02.png?raw=true" width="800" />
</div> 
<div align="center">
  <img src="https://github.com/prodramp/DeepWorks/blob/main/JoJoGAN/images/jojo03.png?raw=true" width="800" />
</div> 
<div align="center">
  <img src="https://github.com/prodramp/DeepWorks/blob/main/JoJoGAN/images/jojo04.png?raw=true" width="800" />
</div> 


### Research Paper and Code 
- [JoJoGAN - GitHub Source Code](https://github.com/mchong6/JoJoGAN)
- [Research Paper - Arxiv](https://arxiv.org/abs/2112.11641)
- [Research Paper PDF Document](https://arxiv.org/pdf/2112.11641.pdf)
- [FFHQ Datasets](https://github.com/NVlabs/ffhq-dataset)
- [Original Nvidia TensorFlow Implementation](https://github.com/NVlabs/stylegan2)
- [PyTorch Implementation](https://github.com/rosinality/stylegan2-pytorch)
- [DLIB Library to process Faces](http://dlib.net/)

### Resources & Articles ###
- https://machinelearningmastery.com/introduction-to-style-generative-adversarial-network-stylegan/
- https://towardsdatascience.com/stylegan-v2-notes-on-training-and-latent-space-exploration-e51cf96584b3
- https://blog.paperspace.com/how-to-set-up-stylegan2-ada-pytorch-on-paperspace/

### Hugging Face Cards for Various GAN Samples
- https://huggingface.co/mfrashad
- https://huggingface.co/spaces/vaibhavarduino/anime-plus
- https://huggingface.co/spaces/akhaliq/JoJoGAN
 
