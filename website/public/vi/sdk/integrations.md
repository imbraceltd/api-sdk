# Tích Hợp

> Sử dụng Imbrace SDKs với React, Next.js, Node.js, FastAPI, asyncio, Django, và Celery.

Các pattern tích hợp ở cấp độ framework cho cả hai SDK. TypeScript bao gồm React, Next.js, và Node.js thuần; Python bao gồm FastAPI, asyncio, Django, và Celery. Luồng OTP login được ghi lại cho cả hai.

Để biết chiến lược credential (api key vs access token, env vars), xem [Xác Thực](/vi/sdk/authentication/) và [Hướng Dẫn Cài Đặt](/vi/getting-started/setup/#configure-credentials).

---

## React (TypeScript)

### Singleton Client

Tạo client một lần bên ngoài component tree và tái sử dụng. Token trong `localStorage` đến từ [luồng OTP login](/vi/sdk/authentication/#luồng-otp-login).

```typescript
// lib/imbrace.ts

export const client = new ImbraceClient({
  accessToken:
    typeof window !== "undefined"
      ? (localStorage.getItem("imbrace_token") ?? undefined)
      : undefined,
});
```

### Custom Hook Fetch Data

```tsx
// hooks/useProducts.ts

export function useProducts(category?: string) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    client.marketplace
      .listProducts({ category })
      .then((res) => setProducts(res.data))
      .catch(setError)
      .finally(() => setLoading(false));
  }, [category]);

  return { products, loading, error };
}
```

```tsx
// components/ProductList.tsx

export function ProductList() {
  const { products, loading, error } = useProducts("electronics");
  if (loading) return <p>Đang tải...</p>;
  if (error) return <p>Lỗi: {error.message}</p>;
  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name} — {p.price} {p.currency}</li>
      ))}
    </ul>
  );
}
```

---

## Next.js (TypeScript)

### API Route (App Router)

```typescript
// app/api/products/route.ts

const client = new ImbraceClient({
  apiKey: process.env.IMBRACE_API_KEY,
});

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get("category") ?? undefined;
  const { data } = await client.marketplace.listProducts({ category });
  return NextResponse.json(data);
}

export async function POST(request: Request) {
  const body = await request.json();
  const product = await client.marketplace.createProduct(body);
  return NextResponse.json(product, { status: 201 });
}
```

`process.env.IMBRACE_API_KEY` nên được set theo cách platform deploy của bạn. Xem [Hướng Dẫn Cài Đặt → Cấu hình credentials](/vi/getting-started/setup/#configure-credentials).

### Server Component (App Router)

```tsx
// app/products/page.tsx

const client = new ImbraceClient({
  apiKey: process.env.IMBRACE_API_KEY,
});

export default async function ProductsPage() {
  const { data: products } = await client.marketplace.listProducts({ limit: 20 });
  return (
    <main>
      <h1>Sản Phẩm</h1>
      <ul>{products.map((p) => <li key={p.id}>{p.name}</li>)}</ul>
    </main>
  );
}
```

---

## Node.js CLI Script (TypeScript)

Cho các script one-shot (data exports, backfills, ad-hoc queries):

```typescript
// scripts/export-contacts.ts

const client = new ImbraceClient();

async function exportContacts() {
  const { data: contacts } = await client.contacts.list({ limit: 1000 });
  writeFileSync("contacts.json", JSON.stringify(contacts, null, 2));
  console.log(`Đã xuất ${contacts.length} liên hệ`);
}

exportContacts().catch(console.error);
```

```bash
npx ts-node scripts/export-contacts.ts
```

---

## FastAPI (Python)

### Per-request Dependency Injection

Pattern đơn giản nhất — một async client per request, lifetime được quản lý bởi dependency:

```python
from fastapi import FastAPI, Depends
from imbrace import AsyncImbraceClient

app = FastAPI()

async def get_imbrace() -> AsyncImbraceClient:
    async with AsyncImbraceClient() as client:
        yield client

@app.get("/products")
async def list_products(client: AsyncImbraceClient = Depends(get_imbrace)):
    result = await client.marketplace.list_products(limit=20)
    return result["data"]

@app.get("/products/{product_id}")
async def get_product(product_id: str, client: AsyncImbraceClient = Depends(get_imbrace)):
    return await client.marketplace.get_product(product_id)

@app.post("/ai/chat")
async def chat(message: str, client: AsyncImbraceClient = Depends(get_imbrace)):
    return await client.ai.complete(
        model="gpt-4o",
        messages=[{"role": "user", "content": message}],
    )
```

### Global Singleton (Tái Sử Dụng Connection Pool)

Để đạt throughput cao hơn, chia sẻ một client cho suốt vòng đời ứng dụng:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from imbrace import AsyncImbraceClient

imbrace: AsyncImbraceClient = None  # type: ignore

@asynccontextmanager
async def lifespan(app: FastAPI):
    global imbrace
    imbrace = AsyncImbraceClient()
    await imbrace.init()  # health check khi khởi động
    yield
    await imbrace.close()

app = FastAPI(lifespan=lifespan)

@app.get("/me")
async def get_me():
    return await imbrace.platform.get_me()
```

---

## asyncio (Python)

### Concurrent Requests

```python
from imbrace import AsyncImbraceClient

async def fetch_dashboard_data():
    async with AsyncImbraceClient() as client:
        me, products, channels = await asyncio.gather(
            client.platform.get_me(),
            client.marketplace.list_products(limit=5),
            client.channel.list_channels(type="group"),
        )
        return {
            "user": me,
            "products": products["data"],
            "channels": channels["data"],
        }

data = asyncio.run(fetch_dashboard_data())
```

### Streaming AI

```python
from imbrace import AsyncImbraceClient

async def stream_response():
    async with AsyncImbraceClient() as client:
        async for chunk in client.ai.stream(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Giải thích async/await trong Python."}],
        ):
            content = chunk["choices"][0]["delta"].get("content", "")
            print(content, end="", flush=True)

asyncio.run(stream_response())
```

---

## Django (Python)

### Synchronous View

```python
# views.py
from django.http import JsonResponse
from imbrace import ImbraceClient, ApiError

def product_list(request):
    with ImbraceClient() as client:
        try:
            result = client.marketplace.list_products(
                category=request.GET.get("category"),
                page=int(request.GET.get("page", 1)),
            )
            return JsonResponse(result)
        except ApiError as e:
            return JsonResponse({"error": str(e)}, status=e.status_code)
```

### Django Settings

```python
# settings.py
IMBRACE_API_KEY = env("IMBRACE_API_KEY")
IMBRACE_ENV = env("IMBRACE_ENV", default="stable")

# utils/imbrace.py
from django.conf import settings
from imbrace import ImbraceClient

def get_client() -> ImbraceClient:
    return ImbraceClient(
        api_key=settings.IMBRACE_API_KEY,
        env=settings.IMBRACE_ENV,
    )
```

---

## Celery (Python)

Với background task workers, tạo client bên trong mỗi task — không chia sẻ giữa các worker:

```python
# tasks.py
from celery import Celery
from imbrace import ImbraceClient, NetworkError

app = Celery("tasks")

@app.task(bind=True, max_retries=3)
def sync_products(self):
    try:
        with ImbraceClient() as client:
            result = client.marketplace.list_products(limit=100)
            for product in result["data"]:
                save_to_db(product)
    except NetworkError as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

> Không chia sẻ một `ImbraceClient` duy nhất giữa các Celery worker — tạo mới trong mỗi task. httpx connection pool không an toàn để chia sẻ giữa các process.

---

## Luồng OTP Login

Luồng OTP về mặt khái niệm giống nhau ở cả hai SDK: yêu cầu OTP cho email, rồi đổi lấy access token. Xem [Xác Thực → luồng OTP login](/vi/sdk/authentication/#luồng-otp-login) để xem toàn bộ vòng đời credential.

```tsx
// components/LoginForm.tsx

const client = new ImbraceClient();

export function LoginForm() {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [step, setStep] = useState<"email" | "otp">("email");

  async function requestOtp() {
    await client.requestOtp(email);
    setStep("otp");
  }

  async function verifyOtp() {
    try {
      await client.loginWithOtp(email, otp);
      window.location.href = "/dashboard";
    } catch (e) {
      if (e instanceof AuthError) alert("OTP không đúng");
    }
  }

  return step === "email" ? (
    
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <button onClick={requestOtp}>Gửi OTP</button>
    
  ) : (
    
      <input value={otp} onChange={(e) => setOtp(e.target.value)} placeholder="Nhập OTP" />
      <button onClick={verifyOtp}>Xác nhận</button>
    
  );
}
```

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from imbrace import AsyncImbraceClient, AuthError

app = FastAPI()

class OtpRequest(BaseModel):
    email: str

class OtpVerify(BaseModel):
    email: str
    otp: str

@app.post("/auth/request-otp")
async def request_otp(body: OtpRequest):
    async with AsyncImbraceClient() as client:
        await client.request_otp(body.email)
    return {"message": "OTP đã được gửi"}

@app.post("/auth/verify-otp")
async def verify_otp(body: OtpVerify):
    async with AsyncImbraceClient() as client:
        try:
            await client.login_with_otp(body.email, body.otp)
            token = client._token_manager.get_token()
            return {"access_token": token}
        except AuthError:
            raise HTTPException(status_code=401, detail="OTP không đúng")
```
