# Finetuning LLM # 



### Using LlamaIndex (previously known as GPT Index)
LlamaIndex (GPT Index) is a project that provides a central interface to connect your LLM's with external data. 

- https://github.com/jerryjliu/llama_index
- https://llamahub.ai/
- https://gpt-index.readthedocs.io/en/latest/reference/readers.html#gpt_index.readers.SimpleDirectoryReader

### Video Tutorial - Fine Tuning LLM with Custom Data (using Open AI GPT) in python
<table class="table table-striped table-bordered table-vcenter">
    <tr>
        <td align="center"><b>🔥&nbsp;Fine Tuning LLM with Custom Data (using Open AI GPT) in python</b></td>
    </tr>
    <tr>
        <td>
            <div>
                
[![Fine Tuning LLM with Custom Data (using Open AI GPT) in python](https://img.youtube.com/vi/6aOzoJKNLKQ/0.jpg)](https://www.youtube.com/watch?v=6aOzoJKNLKQ)

 </tr>
</table>

### finetune.py
```
import os
os.environ["OPENAI_API_KEY"] = 'sk-your_key'

from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader('data').load_data()
index = GPTSimpleVectorIndex(documents)

# save to disk
index.save_to_disk('index.json')


```

### queryindex.py
```
import os
os.environ["OPENAI_API_KEY"] = 'sk-your_key'

from gpt_index import GPTSimpleVectorIndex

# load from disk
index = GPTSimpleVectorIndex.load_from_disk('indexes/index.json')

statement = "start"

while statement != 'exit':
    statement = input('What is your question? > ')
    print(" Your question is - " + statement)
    print("Answer: ")
    print(index.query(statement))

```