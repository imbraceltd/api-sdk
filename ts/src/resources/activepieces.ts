import { HttpTransport } from "../http.js"

export class ActivePiecesResource {
  /**
   * @param base - ActivePieces base URL (gateway/activepieces)
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}  

  /**
   * Generic GET request to ActivePieces backend
   */
  async get(path: string, params?: Record<string, string>): Promise<any> {
    const url = new URL(`${this.base}${path.startsWith('/') ? path : `/${path}`}`)    
    if (params) {
      Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    }
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  /**
   * Generic POST request to ActivePieces backend
   */
  async post(path: string, body: any): Promise<any> {
    const url = `${this.base}${path.startsWith('/') ? path : `/${path}`}`
    return this.http.getFetch()(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /**
   * Generic PUT request to ActivePieces backend
   */
  async put(path: string, body: any): Promise<any> {
    const url = `${this.base}${path.startsWith('/') ? path : `/${path}`}`
    return this.http.getFetch()(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  /**
   * Generic DELETE request to ActivePieces backend
   */
  async delete(path: string): Promise<any> {
    const url = `${this.base}${path.startsWith('/') ? path : `/${path}`}`
    return this.http.getFetch()(url, { method: "DELETE" }).then(r => r.json())
  }
}
