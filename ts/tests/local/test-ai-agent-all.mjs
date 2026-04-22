import { ImbraceClient } from '@imbrace/sdk'

const client = new ImbraceClient({
  accessToken: 'acc_c10f483f-0e45-4966-a275-2fb0356365e7',
  baseUrl: 'https://app-gatewayv2.imbrace.co',
})
const ASSISTANT_ID = 'a5ffe364-c136-40a0-aa49-84866e4d8485'
const ORG_ID = 'org_6d4ae4f2-f75c-4324-9269-c3fec12078cc'

async function test(name, fn) {
  try {
    const result = await fn()
    console.log(`✓ ${name}`, JSON.stringify(result)?.slice(0, 80))
  } catch (e) {
    console.log(`✗ ${name}: [${e.statusCode ?? e.message}]`, e.message?.slice(0, 100))
  }
}

await test('getAgentPromptSuggestion', () => client.aiAgent.getAgentPromptSuggestion(ASSISTANT_ID))
await test('listEmbeddingFiles',       () => client.aiAgent.listEmbeddingFiles())
await test('classifyFile',             () => client.aiAgent.classifyFile({ url: 'https://example.com/test.pdf', mime_type: 'application/pdf' }))
await test('createClientChat',         () => client.aiAgent.createClientChat({
  id: crypto.randomUUID(),
  message: { id: crypto.randomUUID(), role: 'user', parts: [{ type: 'text', text: 'Hello' }] },
  assistantId: ASSISTANT_ID,
  organizationId: ORG_ID,
}))
await test('listClientMessages',       () => client.aiAgent.listClientMessages('fake-id'))
await test('deleteClientChat',         () => client.aiAgent.deleteClientChat('fake-id'))
