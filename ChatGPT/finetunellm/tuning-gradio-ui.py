import gradio as gr
import os
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex
from gpt_index.readers.file.docs_parser import PDFParser
from gpt_index.readers.schema.base import Document


class GPTProcessing(object):
    def __init__(self, ui_obj):
        self.name = "Custom Data Processing with ChatGPT"
        self.description = "Add Custom Data Processing with ChatGPT"
        self.api_key = None
        self.index_folder = "indexdata"
        self.ui_obj = ui_obj
        self.api_key_status = "Error: OpenAI API is not set"
        self.selected_index = None
        self.index_status = "Error: Index is not selected"
        self.index_setup_result = ".... no action..."

    def create_ui(self):
        with self.ui_obj:
            gr.Markdown("Custom Fine-tuning with Large Language Model")
            with gr.Tabs():
                with gr.TabItem("Setup OpenAI Configuration"):
                    with gr.Row():
                        openai_api_key = gr.Textbox(label="OpenAI API Key",
                                                    placeholder="OpenAI API key here..",
                                                    type='password')
                        set_api_action = gr.Button("Setup API Key")
                    with gr.Row():
                        openai_api_stats = gr.Label(self.api_key_status)
                with gr.TabItem("Training/Fine-tuning with Custom Data"):
                    with gr.Row():
                        source_data = gr.File(
                            label="PDF or Text files only",
                            file_count="single",
                            file_types=["file"])
                        index_setup_action = gr.Button("Create Index")
                    with gr.Row():
                        index_setup_result_label = gr.Label(self.index_setup_result)
                with gr.TabItem("Query Custom Data"):
                    with gr.Row():
                        index_listing_action = gr.Button("List all Indexes")
                        index_list_output = gr.Textbox(label="Listed Indexes")
                    with gr.Row():
                        index_file_name = gr.Textbox(label="Select Index")
                        index_selection_action = gr.Button("Load Index")
                    with gr.Row():
                        index_status_label = gr.Label(self.index_status)
                    with gr.Row():
                        query_question = gr.Textbox(label="Enter your question:", lines=5)
                        query_data_action = gr.Button("Get Answer")
                    with gr.Row():
                        query_result_text = gr.Textbox(label="Query Result:", lines=10)

            set_api_action.click(
                self.update_api_status,
                [
                    openai_api_key
                ],
                [
                    openai_api_stats
                ]
            )

            index_setup_action.click(
                self.index_setup_process,
                [
                    source_data
                ],
                [
                    index_setup_result_label
                ]
            )

            index_listing_action.click(
                self.index_listing,
                [

                ],
                [
                    index_list_output
                ]
            )

            index_selection_action.click(
                self.setup_index_from_collection,
                [
                    index_file_name
                ],
                [
                    index_status_label
                ]
            )

            query_data_action.click(
                self.get_answer_from_index,
                [
                    query_question
                ],
                [
                    query_result_text
                ]
            )


    def load_source_data(self, file):
        source_data = []
        data_list = []
        file = file.lower()
        file_extension = os.path.splitext(file)
        if len(file_extension) == 2 and file_extension[1] in ['.pdf', '.txt']:
            if file_extension[1] == '.pdf':
                parser = PDFParser()
                extracted_pdf = parser.parse_file(file)
                data_list.append(extracted_pdf)
                source_data = [Document(d) for d in data_list]
            elif file_extension[1] == '.txt':
                text_file_path = os.path.split(file)
                source_data = SimpleDirectoryReader(text_file_path[0]).load_data()

        return source_data

    def save_index_document(self, source_index, out_file_name):
        try:
            final_out_file = os.path.basename(out_file_name.lower()) + ".json"
            final_out_file_path = os.path.join(os.getcwd(), self.index_folder, final_out_file)
            source_index.save_to_disk(final_out_file_path)
        except:
            final_out_file_path = None

        return final_out_file_path

    def index_setup_process(self, file):
        source_documents = self.load_source_data(file.name)
        status_message = "Error: Unable to create to source document index"
        if len(source_documents) > 0:
            source_index = GPTSimpleVectorIndex(source_documents)
            saved_file = self.save_index_document(source_index, file.name)
            if saved_file is not None:
                status_message = "Success: The index is ready as [" + saved_file + "]"
        return status_message

    def update_api_status(self, api_key):
        if api_key is not None and len(api_key) > 0:
            self.api_key = str(api_key)
            self.api_key_status = str("Success: OpenAI key is set")
            os.environ["OPENAI_API_KEY"] = self.api_key
        return self.api_key_status

    def index_listing(self):
        index_path = os.path.join(os.getcwd(), self.index_folder)
        all_files = os.listdir(index_path)
        if len(all_files) == 0:
            return "No files"
        else:
            return all_files

    def setup_index_from_collection(self, index_name):
        if index_name is not None and len(index_name) > 0 and self.api_key is not None:
            index_path = os.path.join(os.getcwd(), self.index_folder, index_name)
            if os.path.exists(index_path):
                self.selected_index = GPTSimpleVectorIndex.load_from_disk(index_path)
                self.index_status = "Success: Index is set.."
            else:
                self.index_status = "Error: Index path is bad"
        return self.index_status

    def get_answer_from_index(self, query_question):
        query_result = "Error: Unable to get answer to your question"
        if query_question is not None and len(query_question) > 0:
            if self.selected_index:
                query_result = self.selected_index.query(query_question)
        return query_result


    def launch_ui(self):
        self.ui_obj.launch()


if __name__ == '__main__':
    my_app = gr.Blocks()
    gradio_ui = GPTProcessing(my_app)
    gradio_ui.create_ui()
    gradio_ui.launch_ui()
