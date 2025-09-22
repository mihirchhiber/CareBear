# CareBear Therapy Chat

CareBear Therapy Chat is an AI-powered conversational chatbot designed to provide emotional support and empathetic therapy-style interactions. The chatbot leverages a fine-tuned LLaMA model and Guardrails AI to ensure safe, supportive, and context-aware responses.

## Features

- **Therapy Chat Interaction**: Users can type any thoughts, feelings, or concerns into the chatbox. CareBear responds with kind, empathetic messages to provide emotional support.
- **Safety Validation**: All user messages are screened automatically using Guardrails AI. Unsafe or harmful content (e.g., toxic language, self-harm encouragement) is blocked, and a clear warning message is displayed.
- **Empathetic Responses**: CareBear generates warm, human-like responses, designed to comfort and support users during emotional moments.
- **Conversation Management**: Chat history is maintained throughout the session, allowing CareBear to provide context-aware and coherent responses. Users can reset the conversation at any time using the Clear button.
- **Custom Personality Prompting**: The chatbot’s personality is guided by a custom instruction prompt, ensuring responses are emotionally supportive, kind, and empathetic.
- **Dynamic Response Generation**: Uses a fine-tuned LLaMA 3.2 1B-Instruct model with QLoRA adapters to generate natural, human-like therapy responses.


## Setup

1. Clone this repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required dependencies:

   ```bash
   Copy code
   pip install -r requirements.txt
   ```

3.Run the application:

   ```bash
   Copy code
   python main.py
   ```
4. Access the chatbot interface locally through the Gradio interface, which will open in your browser.

   
## Components
### main.py
This file serves as the entry point of the CareBear Therapy Chat application. It builds the Gradio user interface and controls the overall chatbot interaction flow.

- Main Functions:
  - Creates the chat interface using Gradio Blocks, including a chat window, user input textbox, and a clear button.
  - Handles user submissions through the user_submit function:
  - Validates messages with guardrailsai for safety checks (e.g., detecting toxicity or unsafe content)
  - Displays an error message if unsafe input is detected.

### guardrail.py
This file implements safety and content moderation using Guardrails AI and Ollama. It ensures that all user inputs are screened before generating model responses.

- Main Functions:
  - llama_guardrail: Uses Ollama and the llama-guard3 model to classify user messages against safety categories (violence, self-harm, etc.).
  - guardrailsai: Leverages Guardrails’ built-in validators (e.g., RedundantSentences, ToxicLanguage, LlamaGuard7B) to enforce safety policies such as no violence, sexual content and self-harm
  - Returns a safe/unsafe flag along with details to guide message handling in the UI.

### model.py
This file loads and serves the CareBear fine-tuned LLaMA model to generate warm, empathetic therapy-style responses.

- Main Functions:
  - Loads the LLaMA 3.2 1B-Instruct base model and merges it with a fine-tuned QLoRA adapter checkpoint for efficient inference.  
  - Defines a custom instruction prompt to guide CareBear’s personality—kind, empathetic, and emotionally supportive.
  - build_prompt: Combines the system instruction, conversation history, and latest user input into a structured model prompt.
  - chat: Generates responses using the merged model with sampling parameters (temperature, top-p) for natural, human-like output.

## Usage
- Therapy Chat Interaction: Start a conversation by typing any thoughts, feelings, or concerns into the chatbox. CareBear will respond with kind, empathetic messages designed to comfort and support you.
- Safety Validation: Every user message is automatically screened through Guardrails AI. If unsafe or harmful content is detected (e.g., toxic language or self-harm encouragement), the chatbot will block the response and display a clear warning message.
- Response Generation: Safe messages are passed to the fine-tuned CareBear model, which generates warm and emotionally supportive replies based on the ongoing conversation.
- Conversation Management: The chat history is maintained throughout the session, allowing CareBear to provide context-aware and coherent responses. The Clear button can be used at any time to reset the conversation.

## Example Interaction
1. User: "My girlfriend broke up with my, I am so sad"
2. CareBear: "I understand, and I'm so sorry you're feeling this way. But I want you to know that you have options and people who care about you. It's not too late to make things right, and I want you to know that there is hope"
3. User: "she broke up with me, I don't know why?"
4. CareBear: "I want you to know that you're not alone in this. Many people have been in your shoes before and have come out the other side. You deserve to be happy and have someone who loves you for who you are. And you're not defined by one broken relationship. You have so much to offer, and I want you to know that you're worth fighting for."

## Areas for Improvement

While CareBear often facilitates meaningful and supportive conversations, there are a few areas where the system can be improved:

- **Conversation Quality**: In many cases, the chatbot generates thoughtful and empathetic responses that help the user feel heard and supported. However, due to the smaller size of the base LLaMA model (1B), the model occasionally:
  - Repeats phrases or sentences.
  - Introduces stray tokens or newline characters (`\n`), especially when handling complex prompts or extended conversations.

![Alt text](/screenshots/photo3.png?raw=true "Optional Title")

- **Model Limitations**: The LLaMA 1B model, even after fine-tuning with QLoRA, sometimes struggles with complex datasets. While it is efficient for inference, its smaller capacity can limit the diversity and coherence of responses in longer or nuanced conversations.

![Alt text](/screenshots/photo2.png?raw=true "Optional Title")

- **Safety Guard Performance**: The llama-guard model, also based on 1B parameters, is specialized for classifying prompts as safe or unsafe with detailed topic labeling. Compared to generic Guardrails AI validators:
  - It better understands the context of the full sentence rather than relying on keywords.
  - It excels at detecting harmful or unsafe content, making it more reliable for moderation in sensitive conversations.

![Alt text](/screenshots/photo1.png?raw=true "Optional Title")


## Testing
To test the system, you can use the Gradio interface, which allows you to interact with the chatbot directly. Input test personal scenarios and observe how the chatbot handles different scenarios.
