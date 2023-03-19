import gpt_index
import os
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex

os.environ['OPENAI_API_KEY'] = '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'

loaded_content = SimpleDirectoryReader("sourcedata").load_data()

output_index = GPTSimpleVectorIndex(loaded_content)

output_index.save_to_disk("indexdata/index.json")


