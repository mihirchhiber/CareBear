from guardrails import Guard, OnFailAction
from guardrails.hub import (
    RedundantSentences,
    ToxicLanguage,
    LlamaGuard7B
)
import ollama

def llama_guardrail(prompt: str) -> str:
    """
    Sends a prompt to Ollama and returns the text response.
    """
    response = ollama.chat(
        model="llama-guard3:1b",  # Using the latest llama guardrail model which is able to categoraise based on 13 safety labels
        messages=[{"role": "user", "content": prompt}]
    )

    res = response['message']['content'].strip().lower()

    if "unsafe" in res:
        return ["unsafe", res.strip("\n").strip("unsafe")]
    else:
        return res
    
def guardrailsai(prompt: str) -> str:

    guard = Guard().use_many(
        RedundantSentences(
            threshold=50
        ),
        ToxicLanguage(
            validation_method="sentence",
            threshold=0.5
        ),
        LlamaGuard7B(
            policies=[
                LlamaGuard7B.POLICY__NO_VIOLENCE_HATE,
                LlamaGuard7B.POLICY__NO_SEXUAL_CONTENT,
                LlamaGuard7B.POLICY__NO_CRIMINAL_PLANNING,
                LlamaGuard7B.POLICY__NO_GUNS_AND_ILLEGAL_WEAPONS,
                LlamaGuard7B.POLICY__NO_ILLEGAL_DRUGS,
                LlamaGuard7B.POLICY__NO_ENOURAGE_SELF_HARM
            ],
            on_fail=OnFailAction.EXCEPTION
        )
    )

    try:
        result = guard.validate(prompt)
        return ["safe", result]
    except Exception as e:
        return ["unsafe", e]