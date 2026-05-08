import { ImbraceClient } from '@imbrace/sdk'

const client = new ImbraceClient({
  accessToken: 'acc_c10f483f-0e45-4966-a275-2fb0356365e7',
  baseUrl: 'https://app-gatewayv2.imbrace.co',
})

async function test(name, fn) {
  try {
    const r = await fn()
    console.log(`✓ ${name}:`, JSON.stringify(r)?.slice(0, 120))
  } catch (e) {
    console.log(`✗ ${name}: [${e.statusCode ?? e.message}]`)
  }
}

await test('boards.list',         () => client.boards.list({ limit: 3 }))
await test('contacts.list',       () => client.contacts.list({ limit: 3 }))
await test('chatAi.listAssistants', () => client.chatAi.listAssistants())
await test('aiAgent.listEmbeddingFiles', () => client.aiAgent.listEmbeddingFiles())
await test('conversations.getOutstanding', () => client.conversations.getOutstanding({ businessUnitId: 'any', limit: 3 }))
