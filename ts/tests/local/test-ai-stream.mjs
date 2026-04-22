/**
 * answerQuestion (RAG) — non-streaming + streaming test
 * Usage: node test-ai-stream.mjs
 */

import { ImbraceClient } from '@imbrace/sdk'

const ACCESS_TOKEN = process.env.IMBRACE_ACCESS_TOKEN  || 'acc_c8c27f3b-e147-4735-b641-61e8d3706692'
const GATEWAY      = process.env.IMBRACE_GATEWAY_URL   || 'https://app-gatewayv2.imbrace.co'
const ASSISTANT_ID = 'a5ffe364-c136-40a0-aa49-84866e4d8485'
const QUESTION     = 'What can you help me with?'

const client = new ImbraceClient({ accessToken: ACCESS_TOKEN, baseUrl: GATEWAY })
const ai = client.ai

let passed = 0, failed = 0

function ok(label, detail = '') {
  console.log(`  ✓ ${label}${detail ? `  →  ${String(detail).slice(0, 120)}` : ''}`)
  passed++
}

function fail(label, err) {
  console.error(`  ✗ ${label}: ${err?.message ?? JSON.stringify(err)}`)
  failed++
}

// ─────────────────────────────────────────────────────────────────────────────
// Non-streaming
// ─────────────────────────────────────────────────────────────────────────────

// console.log('\n[1] answerQuestion — non-streaming')
try {
  const res = await ai.answerQuestion({
    text: QUESTION,
    assistant_id: ASSISTANT_ID,
    streaming: false,
    thread_id: '',
    knowledge_hubs: [],
    file_ids: [],
    board_ids: [],
    conversation_id: '',
  })
  ok('answerQuestion(streaming: false)', `thread_id=${res.thread_id} message="${res.message}"`)
} catch (e) { fail('answerQuestion(streaming: false)', e) }

// ─────────────────────────────────────────────────────────────────────────────
// Streaming
// ─────────────────────────────────────────────────────────────────────────────

console.log('\n[2] answerQuestion — streaming')
try {
  let full = ''
  let chunkCount = 0

  for await (const chunk of ai.answerQuestion({
    text: QUESTION,
    assistant_id: ASSISTANT_ID,
    streaming: true,
  })) {
    // console.log(chunk.message)
    full += chunk.message
    chunkCount++
  }

  ok(`received ${chunkCount} chunks`, `"${full.slice(0, 1000)}"`)
} catch (e) { fail('answerQuestion(streaming: true)', e) }

// ─────────────────────────────────────────────────────────────────────────────

// console.log(`\n${'─'.repeat(55)}`)
// console.log(`  ${passed} passed  |  ${failed} failed`)
if (failed > 0) process.exit(1)
