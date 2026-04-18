#!/usr/bin/env python3
# \"\"\"Demo Imbrace SDK - 3 Environments + ServiceRegistry.\"""

from imbrace import ImbraceClient

def demo_client(env):
    print("\\n" + "="*60)
    print("🚀 Demo ImbraceClient(env='%s') - ServiceRegistry Pattern" % env)
    print("="*60)
    
    client = ImbraceClient(
        env=env,
        organization_id="demo-org-id",
        check_health=True
    )
    
    print("Gateway:", client.health.base)
    print("Channel:", client.channel.base)
    print("Boards:", client.boards.base)
    print("IPS:", client.ips.base)
    
    print("\\n✅ Health check OK!")
    print("\\n✅ SDK ready for production - ServiceRegistry + 3 Envs!")
    
    client.close()

if __name__ == "__main__":
    for env in ["develop", "sandbox", "stable"]:
        demo_client(env)

