import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Model and Tokenizer
BASE_MODEL = "meta-llama/Llama-3.2-1B-Instruct"
CHECKPOINT = r"C:\Users\m\Documents\GitHub\CareBear\model_finetuning_and_safety\shawgpt-llama3-qlora\shawgpt-llama3-qlora\checkpoint-469"

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token

# Load base model in 4bit
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, CHECKPOINT)
model = model.merge_and_unload()      # merge for inference
model.eval()

INSTRUCTION = (
    "CareBear, a warm and gentle therapy bear you can talk to when you need comfort, "
    "responds with kindness and empathy in a soothing, uplifting tone. "
    "CareBear listens carefully, offers thoughtful support, and provides practical tips "
    "for emotional well-being when appropriate. It communicates in clear, compassionate "
    "language and matches the length of its replies to the person’s message."
)

def build_prompt(history, user_input):
    """Combine instruction + chat history + new user input."""
    dialogue = ""
    for h, a in history:
        dialogue += f"User: {h}\nCareBear: {a}\n"
    dialogue += f"User: {user_input}\nCareBear:"
    return f"<s>[INST] {INSTRUCTION}\n{dialogue}\n[/INST]\n"

# Chat function
def chat(user_message, history):
    prompt = build_prompt(history, user_message)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
        )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the last assistant turn if model echoes prompt
    if "CareBear:" in text:
        text = text.split("CareBear:")[-1].strip()
    return text