from imbrace import ImbraceClient, extract_api_key
from dotenv import load_dotenv
import os

load_dotenv()

# --- Cách 1: Dùng thẳng API Key string ---
client = ImbraceClient(
    api_key=os.getenv("IMBRACE_API_KEY"),
    # base_url mặc định: https://app-gatewayv2.imbrace.co
)

# Hoặc --- Cách 2: Từ response của auth endpoint ---
# import httpx
# res = httpx.get(
#     "https://app-gatewayv2.imbrace.co/auth/key",
#     headers={"X-Api-Key": "your-raw-key"}
# ).json()
# client = ImbraceClient(api_key=extract_api_key(res))

# List sessions
sessions = client.sessions.list()
print("Sessions:", sessions)

# Create session and send a message
session = client.sessions.create(directory=os.getcwd())
response = client.messages.send(
    session["id"],
    parts=[{"type": "text", "text": "Hello from Imbrace Python SDK!"}],
    directory=os.getcwd(),
)
print("Response:", response)

client.close()
