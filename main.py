import os
from pathlib import Path

# Load .env into the environment
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

from sarvamai import SarvamAI

# Initialize Sarvam client reading key from environment
client = SarvamAI(api_subscription_key=os.environ.get("SARVAM_API_KEY"))

# Make chat completion call
response = client.chat.completions(
    model="sarvam-105b-conversations",
    messages=[
        {"role": "user", "content": "Hello! Say hi in one short sentence."}
    ],
)

# Print the reply
print(response.choices[0].message.content)
