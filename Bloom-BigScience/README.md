# Bloom - BigScience  Language Model #

This hands-on programming tutorial with step by step implementation of Bloom Large Language Text Generation Model will guide you building your own text generation application in Google Colab environment. 

You will also learn to solve 3 different problems while working on this tutorial:

### Error 1 ###
- RuntimeError: Expected all tensors to be on the same device, but found at least two devices, cpu and cuda:0! (when checking argument for argument index in method wrapper__index_select)

Solution:
- The models were instantiated on CPU however the tokenization was done at the GPU so when the language modeling request was made the tensors were not found at one place either in CPU or on GPU. The solution was to restart the environment and reload all the resources properperly at the GPU.


### Error 2 ###
- AttributeError: 'BaseModelOutputWithPastAndCrossAttentions' object has no attribute 'logits'

Solution:
- The language model object which you have loaded may or may not have the language modeling function so this error may occur if you do now use the correct model with language modeling support. In our case the first model we loaded does not have the correct language modelling support so we changed the class to load the model with language modeling support and it worked. 

### Error 3 ###
- GPU Memory Exception while loading Bloom models with tokenizer

Solution:
- Because I am using free version of Google Colab which has around 1GB GPU RAM so loading multiple large models cause memory exception. The solution is to load only those models which can be fit into the given GPU memory or use the CPU if that is an acceptable solution. 


<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp;Bloom (Text Generation Large Language Model - LLM):&nbsp; Step by step implementation </b></td>
    </tr>
    <tr>
        <td>
            <div>                

[![Bloom (Text Generation Large Language Model - LLM): Step by step implementation](https://img.youtube.com/vi/HOiBaH9gAlU/0.jpg)](https://www.youtube.com/watch?v=HOiBaH9gAlU)

</tr>
</table>

## Resource ## 
Latest Bloom LLM Model (176B Paramters):
- https://huggingface.co/bigscience/bloom-1b7

## List of text-generation models at Hugging Face
- https://huggingface.co/models?pipeline_tag=text-generation

## Other similar language model ##
- https://huggingface.co/EleutherAI/gpt-neo-2.7B
- https://huggingface.co/facebook/opt-1.3b
- https://huggingface.co/gpt2
- https://huggingface.co/bigscience/bloom-1b3




## Articles  ##
- https://www.infoq.com/news/2022/07/bigscience-bloom-nlp-ai/
- 
