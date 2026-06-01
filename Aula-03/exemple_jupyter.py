from groq import Groq
import pandas as pd

Client = Groq (
    api_key = "YOUR_API_KEY")

response = client.chat.completions.create(
    model = "openai/gpt-oss-120b"),
messages = [
    {
        "role": "user",
        "content": "Liste as 5 linguagens utilizadas em IA."
        }
        ]
)

texto = response.choise[0].message.content

df = pd.DataFrame({
    "Resposta": [texto]
    })