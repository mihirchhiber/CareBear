import gradio as gr
from guardrail import llama_guardrail
# from guardrail import guardrailsai
from model import chat

with gr.Blocks() as demo:
    gr.Markdown("## 🧸 CareBear Therapy Chat")
    chatbot = gr.Chatbot(label="CareBear Chat")
    msg = gr.Textbox(placeholder="Type your message...")
    clear = gr.Button("Clear")

    def user_submit(message, chat_history):
        check = llama_guardrail(message)
        # check = guardrailsai(message)

        if isinstance(check, list) and check[0] == "unsafe":
            reason = check[1] if len(check) > 1 else "This message is not allowed."
            # First append the *user* message
            chat_history.append((message, None))
            # Then append a big *bot* error message
            chat_history.append((
                None,
                f"🚨 **Unsafe message detected!**\n\n> {reason}"
            ))
            return "", chat_history

        # Safe → normal reply
        reply = chat(message, chat_history)
        chat_history.append((message, reply))
        return "", chat_history

    msg.submit(user_submit, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: ("", []), None, [msg, chatbot], queue=False)

demo.launch()
