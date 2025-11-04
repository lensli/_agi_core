import gradio as gr
from lib.openai import once_chat
with gr.Blocks() as deelark_pre:
    chat_bot = gr.Chatbot(type="messages")
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chat_bot])

    msg.submit(once_chat,[msg,chat_bot],[msg,chat_bot])
deelark_pre.launch(share=False)
