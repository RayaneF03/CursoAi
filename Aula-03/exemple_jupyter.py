from groq import Groq
import pandas as pd

client = Groq(
    api_key = "APIAI"
)

response = client.chat.completions.create(
    model = "openai/gpt-oss-120b",
    messages = [
        {
            "role": "user",
            "content": "Liste as 5 linguagens utilizadas em IA."
        }
    ] 
)

texto = response.choices[0].message.content

df = pd.DataFrame({
    "Resposta": [texto]
})

print(texto)