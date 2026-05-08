import { ImbraceClient } from '@imbrace/sdk'

const client = new ImbraceClient({
  accessToken: 'acc_c10f483f-0e45-4966-a275-2fb0356365e7',
  baseUrl: 'https://app-gatewayv2.imbrace.co',
})

const ts = Date.now()
let createdId = null

async function step(name, fn) {
  console.log(`\n──── ${name} ────`)
  try {
    const r = await fn()
    console.log(JSON.stringify(r, null, 2))
    return r
  } catch (e) {
    console.log(`✗ ERROR: [${e.statusCode ?? e.message}]`)
    return null
  }
}

console.log(`\n=== chatAi AI Agent CRUD lifecycle (ts=${ts}) ===`)

const created = await step('createAiAgent', () =>
  client.chatAi.createAiAgent({
    name: `SDK_RENAME_TEST_${ts}`,
    workflow_name: `sdk_rename_test_${ts}`,
    provider_id: 'system',
    model_id: 'gpt-4o',
    description: 'rename verification — auto-deleted',
  })
)
createdId = created?.id ?? null

if (createdId) {
  await step('getAiAgent', () => client.chatAi.getAiAgent(createdId))

  await step('listAiAgents (full list)', () => client.chatAi.listAiAgents())

  await step('updateAiAgentInstructions', () =>
    client.chatAi.updateAiAgentInstructions(createdId, 'Updated instructions.')
  )

  await step('updateAiAgent (rename)', () =>
    client.chatAi.updateAiAgent(createdId, {
      name: `SDK_RENAME_TEST_${ts}_renamed`,
      workflow_name: `sdk_rename_test_${ts}`,
    })
  )

  await step('deleteAiAgent', () => client.chatAi.deleteAiAgent(createdId))
}

console.log('\n=== Done ===')
