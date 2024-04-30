

from langchain.chains import LLMChain
from langchain_community.llms import GradientLLM
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from gradientai import Gradient

os.environ['GRADIENT_ACCESS_TOKEN'] = "IuQrYCURHsRzzk1BgSDy3xn3V97walUO"
os.environ['GRADIENT_WORKSPACE_ID'] = "d87be754-5abb-4085-97f9-556d00e71fbd_workspace" #"1b99bbdd-1360-4321-a152-fc8822334cd0_workspace"

fine_tuned_Model_Id = "d189f721-ae17-4545-a0ad-f95194e857f5_model_adapter"  #  initializes a GradientLLM with our fine-tuned model by specifying our model ID.

gradient =  Gradient()

base_model = gradient.get_base_model(base_model_slug="nous-hermes2")
print(base_model.id)


llm = GradientLLM(
    model=base_model.id,
    model_kwargs=dict(max_generated_token_count=128),
)




#template = """### Instruction: {Instruction} \n\n### Response:"""

template = """You are a AI having a conversation with a human.
{chat_history}
Human: {Instruction}
Chatbot:"""

prompt = PromptTemplate(template=template, input_variables=["Instruction", 'chat_history'])

memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True,   memory=memory )



from http.server import BaseHTTPRequestHandler, HTTPServer
import json, threading

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Extract the data received from the HTML form
            received_data = data.get('data')

            print(received_data)

            if received_data.startswith("image_Bit data:"):


            """

            Answer = llm_chain.invoke(input=f"{received_data}")

            # Process the received data (for demonstration, just echoing it back)
            processed_data = Answer['text']

            # Print the received data and the processed data
            print("Data received from HTML:", received_data)
            print("Processed data:", processed_data)
            """
            processed_data = " Img Recived"
            # Send a response back to the client
            response_data = {'message': 'Data received and processed successfully', 'processed_data': processed_data}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_error(404, "Not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    def run():
        server_address = ('localhost', 8080)
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.serve_forever()
    threading.Thread(target=run).start()

if __name__ == '__main__':
    run_server()
    print("hezron")
