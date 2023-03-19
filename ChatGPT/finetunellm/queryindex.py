import gpt_index
import os
from gpt_index import GPTSimpleVectorIndex

os.environ['OPENAI_API_KEY'] = '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'

loaded_index = GPTSimpleVectorIndex.load_from_disk("indexdata/index.json")

prompt = "what is this text about?"

while prompt != 'exit':
    prompt = input("Prompt > ")
    result = loaded_index.query(prompt)
    print(result)
