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
    console.log(`✗ ${name}: [${e.statusCode ?? e.constructor.name}] ${e.message?.slice(0, 100)}`)
  }
}

// Test with a dummy email — just want to see if the endpoint is reachable
await test('requestOtp',   () => client.requestOtp('test@example.com'))
await test('loginWithOtp', () => client.loginWithOtp('test@example.com', '000000'))
await test('login',        () => client.login('test@example.com', 'wrongpassword'))
await test('setAccessToken + boards.list', async () => {
  client.setAccessToken('acc_c10f483f-0e45-4966-a275-2fb0356365e7')
  return client.boards.list({ limit: 1 })
})
await test('clearAccessToken', () => {
  client.clearAccessToken()
  return Promise.resolve('ok')
})
