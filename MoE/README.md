# MoE (Mixture of Experts) # 

<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp;YouTube Video:&nbsp; Research Paper Deep Dive - The Sparsely-Gated Mixture-of-Experts (MoE)</b></td>
    </tr>
    <tr>
        <td>
            <div>
                
[![Research Paper Deep Dive - The Sparsely-Gated Mixture-of-Experts (MoE)](https://img.youtube.com/vi/ADooiJ9V7jo/0.jpg)](https://www.youtube.com/watch?v=ADooiJ9V7jo)

  </tr>
</table>

<div align="center">
  <img src="https://github.com/prodramp/DeepWorks/blob/main/MoE/images/Moe-processing.png" width="1000" />
</div> 
<div align="center">
  <img src="https://github.com/prodramp/DeepWorks/blob/main/MoE/images/moe-atchitecture.png" width="700" />
</div> 

### The Problem: ###

We already know that neural networks can  achieve impressive results on a wide range of tasks, such as image classification, machine translation, and protein folding prediction, with the use of inductive biases such as convolutions or sequence attention), increasingly large datasets, and more specialized hardware. The magic behind these amazing results are super massive models with massive collection of paramterrs. 

We all know that large model sizes is necessary for strong generalization and robustness, so training 
large models while limiting resource requirements is becoming increasingly important. 

There is a hidden problem underneath these superstar, eyepoping results and the problem is significant use of computation resources or the requirements, which includes supermassive hardware and that includes logisting, cost, power requirement, and top of the above feasibity to even move it outside labs..

### The solution:

One promising approach is to use conditional computation: 
- Rather than activating the whole network for every single input, different parts of the model are activated for different inputs. 
- Most import things to note here is that MoEs is used a general purpose neural network component.

#### What everybody wants:

- Scale up the model.... 
- Adding model capacity (scaling up) without adding computations resourcs

### Research Papers & GitHub Source Code(s) ###
- https://github.com/davidmrau/mixture-of-experts
- [Research Paper PDF](https://openreview.net/pdf?id=B1ckMDqlg) 
- [Arxiv:1701.06538](https://arxiv.org/abs/1701.06538)
- https://github.com/jsuarez5341/Efficient-Dynamic-Batching

### Resources ###
- [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://research.google/pubs/pub45929/)
- [Scaling Vision with Sparse Mixture of Experts](https://ai.googleblog.com/2022/01/scaling-vision-with-sparse-mixture-of.html)
- [LIMoE](https://ai.googleblog.com/2022/06/limoe-learning-multiple-modalities-with.html)
- [Pathways](https://blog.google/technology/ai/introducing-pathways-next-generation-ai-architecture)
- [Vision-MoE](https://ai.googleblog.com/2020/12/transformers-for-image-recognition-at.html)
- [Task-MoE](https://ai.googleblog.com/2022/01/learning-to-route-by-task-for-efficient.html)
- [large model sizes might be necessary: A Universal Law of Robustness via Isoperimetry: ](https://arxiv.org/pdf/2105.12806.pdf)

