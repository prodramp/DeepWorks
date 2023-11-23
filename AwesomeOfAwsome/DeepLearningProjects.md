# A Collection of Deep Learning Projects worth giving sharp consideration 

## https://github.com/Project-MONAI
MONAI is a PyTorch-based, open-source framework for deep learning in healthcare imaging, part of PyTorch Ecosystem. Its ambitions are:
 - developing a community of academic, industrial and clinical researchers collaborating on a common foundation;
 - creating state-of-the-art, end-to-end training workflows for healthcare imaging;
 - providing researchers with the optimized and standardized way to create and evaluate deep learning models.

## https://github.com/DeepGraphLearning/torchdrug/
TorchDrug is a PyTorch-based machine learning toolbox designed for several purposes.
 - Easy implementation of graph operations in a PyTorchic style with GPU support
 - Being friendly to practitioners with minimal knowledge about drug discovery
 - Rapid prototyping of machine learning research

## https://github.com/riven314/DeepLearning-Navigation
This is a deep learning-based local navigation system for the visually impaired users. The system is prototyped in Python and it offers 3 special features:
 - A segmentation module with low latency (around 20 FPS) and reliable segmentation performance
 - A scene understanding module for summarising spatial scene into grid of objects
- An Obstacle avoidance module for detection of closest obstacle


## https://github.com/BandaiNamcoResearchInc/Bandai-Namco-Research-Motiondataset
The datasets contain a diverse range of contents such as daily activities, fighting, and dancing; with styles such as active, tired, and happy. These can be used as training data for MST models. The animation below shows examples of visualized motions.

Currently, two datasets are available in this repository and are both located under the dataset directory.
- Bandai-Namco-Research-Motiondataset-1 (Details)
  - 17 types of wide-range contents including daily activities, fighting, and dancing.
  - 15 styles that include expression variety.
  - A total of 36,673 frames.


# Code (config.json)

  ```
  {
  "architectures": [
    "LlamaForCausalLM"
  ],
  "bos_token_id": 1,
  "eos_token_id": 2,
  "hidden_act": "silu",
  "hidden_size": 4096,
  "initializer_range": 0.02,
  "intermediate_size": 11008,
  "max_position_embeddings": 4096,
  "model_type": "llama",
  "num_attention_heads": 32,
  "num_hidden_layers": 32,
  "num_key_value_heads": 32,
  "pad_token_id": 0,
  "pretraining_tp": 1,
  "rms_norm_eps": 1e-05,
  "rope_scaling": null,
  "tie_word_embeddings": false,
  "torch_dtype": "float16",
  "transformers_version": "4.31.0.dev0",
  "use_cache": true,
  "vocab_size": 32000
}

  ```
