import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = 'acc_c10f483f-0e45-4966-a275-2fb0356365e7'
const GATEWAY      = 'https://app-gatewayv2.imbrace.co'
const ASSISTANT_ID = 'a5ffe364-c136-40a0-aa49-84866e4d8485'
const ORG_ID       = 'org_6d4ae4f2-f75c-4324-9269-c3fec12078cc'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, gateway: GATEWAY })

console.log('Testing streamChat (token streaming)...')
// user_id omitted — SDK fetches it automatically via chat-client/auth/user
const resp = await client.aiAgent.streamChat({
  assistant_id: ASSISTANT_ID,
  organization_id: ORG_ID,
  messages: [{ role: 'user', content: 'Say hello in one sentence.' }],
})

console.log('Status:', resp.status)
let tokenCount = 0
for await (const chunk of resp.body) {
  const text = new TextDecoder().decode(chunk)
  for (const line of text.split('\n')) {
    if (line.startsWith('data: ') && line !== 'data: [DONE]') {
      try {
        const event = JSON.parse(line.slice(6))
        if (event.type === 'text-delta') {
          process.stdout.write(event.delta)
          tokenCount++
        }
      } catch {}
    }
  }
}
console.log(`\n\n✓ ${tokenCount} text-delta chunks received`)
