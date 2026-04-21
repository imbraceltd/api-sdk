from imbrace import ImbraceClient, extract_api_key
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize client with explicit API Key (e.g. from environment)
api_key = os.environ.get("IMBRACE_API_KEY")
if not api_key:
    print("Warning: IMBRACE_API_KEY not set")

client = ImbraceClient(
    api_key=api_key,
)


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
