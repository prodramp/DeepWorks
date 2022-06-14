# ruDALL-E - Text 2 Image Transformer (Open Source) # 

The ruDALL-E is an open-source text-to-image transformer mode with following versions:
- ruDALL-E  XL model, with 1.3 billion parameters (Open source in 3 different versions)
    - All 3 XL models are available at Hugging Face below:
    - [ruDALL-E Malevich (XL)](https://huggingface.co/sberbank-ai/rudalle-Malevich)
    - [ruDALL-E Emojich (XL)](https://huggingface.co/sberbank-ai/rudalle-Emojich)
    - [ruDALL-E Surrealist (XL)](https://huggingface.co/shonenkov-AI/rudalle-xl-surrealist)
- ruDALL-E XXL model, with 12.0 billion parameters 

<div align="center">
  <img src="https://github.com/prodramp/DeepWorks/blob/main/ruDALL-E/images/ruDALL-e.png?raw=true" width="1000" />
</div> 

### GitHub Repo ###
- https://github.com/ai-forever/ru-dalle
- Quick Try - https://rudalle.ru/en/

### Code Sample - How to use it at Google Colab ###

'''
!pip install rudalle

!cat ru-dalle/requirements.txt
!pip install -r ru-dalle/requirements.txt 


from rudalle import get_rudalle_model, get_tokenizer, get_vae, get_realesrgan

from rudalle.pipelines import generate_images, show, super_resolution

import torch
print('Torch', torch.__version__, 'CUDA', torch.version.cuda)
print('Device:', torch.device('cuda:0'))

device = 'cuda:0'
tokenizer = get_tokenizer()
dalle = get_rudalle_model('Malevich', pretrained=True, fp16=True, device=device) 
vae = get_vae().to(device)

text = 'a penguin is running in desert on a boat'
pil_images, _ = generate_images(text, tokenizer, dalle, vae, top_k=1024, top_p=0.99, images_num=12)
show(pil_images, 12)


realesrgan = get_realesrgan('x2', device=device)
super_images = super_resolution(pil_images, realesrgan)
show(super_images)
'''


### 
- [Zero-Shot Text-to-Image Generation: https://arxiv.org/pdf/2102.12092.pdf](https://arxiv.org/pdf/2102.12092.pdf)
- [Attention is all you need: https://arxiv.org/pdf/1706.03762.pdf](https://arxiv.org/pdf/1706.03762.pdf)

### Google (Vision Transformer (ViT)) - An Image is Worth 16x16 Words ###
- https://arxiv.org/abs/2010.11929
- https://huggingface.co/docs/transformers/model_doc/vit
- https://github.com/google-research/vision_transformer

Other Helpful Resources:
- https://openai.com/blog/dall-e/
- https://openai.com/dall-e-2/
- https://habr.com/en/company/sberbank/blog/589673/
- https://www.marktechpost.com/2022/06/06/researchers-introduce-rudall-e-for-generating-images-from-text-in-russia/
- https://medium.com/analytics-vidhya/understanding-the-vision-transformer-and-counting-its-parameters-988a4ea2b8f3
