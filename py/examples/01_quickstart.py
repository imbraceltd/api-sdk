import os
from imbrace import ImbraceClient

client = ImbraceClient(
    api_key=os.environ["IMBRACE_API_KEY"],
    organization_id=os.environ.get("IMBRACE_ORG_ID"),
    env="stable",
)

channels = client.channel.list()
print("Channels:", channels)

client.close()
