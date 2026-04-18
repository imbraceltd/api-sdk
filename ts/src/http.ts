import { TokenManager } from "./auth/token-manager.js";
import { AuthError, ApiError, NetworkError } from "./errors.js";

/** Detect if a token is a JWT (3 dot-separated base64 parts, starts with eyJ).
 *  Legacy opaque tokens like 'login_acc_...' always return false.
 */
function isJwt(token: string): boolean {
  const parts = token.split(".");
  return parts.length === 3 && token.startsWith("eyJ");
}

interface TransportOptions {
  apiKey?: string;
  timeout: number;
  tokenManager: TokenManager;
  organizationId?: string;
}

export class HttpTransport {
  constructor(private readonly opts: TransportOptions) {}

  public clearApiKey(): void {
    this.opts.apiKey = undefined
  }

  private async sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  public getFetch(): typeof fetch {
    return async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
      let retries = 0;
      const maxRetries = 2;

      while (true) {
        const controller = new AbortController();
        const parentSignal = init?.signal;
        
        let timeoutId: ReturnType<typeof setTimeout> | undefined;
        
        if (parentSignal?.aborted) {
          throw new NetworkError("Request aborted by user");
        }

        const abortListener = () => controller.abort();
        if (parentSignal) {
          parentSignal.addEventListener('abort', abortListener);
        }

        timeoutId = setTimeout(() => controller.abort(), this.opts.timeout);
        
        const reqInit: RequestInit = {
          ...init,
          signal: controller.signal,
          headers: new Headers(init?.headers),
        };

        const headers = reqInit.headers as Headers;
        const token = this.opts.tokenManager.getToken();

        if (this.opts.apiKey) {
          // API Key mode: server-to-server, org resolved by gateway from key
          headers.set("x-api-key", this.opts.apiKey);
        } else if (token && this.opts.organizationId && isJwt(token)) {
          // JWT Bearer mode: auth-service JWT + org scope (only for real JWTs)
          headers.set("authorization", `Bearer ${token}`);
          headers.set("x-organization-id", this.opts.organizationId);
        } else if (token) {
          // Legacy access token mode (opaque tokens like login_acc_...)
          headers.set("x-access-token", token);
        }

        try {
          const res = await globalThis.fetch(input, reqInit);
          
          if (timeoutId) clearTimeout(timeoutId);
          if (parentSignal) parentSignal.removeEventListener('abort', abortListener);

          if (res.ok) {
            return res;
          }

          if (res.status === 401 || res.status === 403) {
            if (this.opts.apiKey) {
              throw new AuthError("Invalid or expired API key (x-api-key).");
            } else if (token && this.opts.organizationId && isJwt(token)) {
              throw new AuthError("Invalid or expired JWT token (Authorization: Bearer) or organizationId not in token.");
            } else if (token) {
              throw new AuthError("Invalid or expired access token (x-access-token).");
            }
            throw new AuthError("No credentials provided — set accessToken= (user login) or apiKey= (server-to-server).");
          }

          if ((res.status === 429 || res.status >= 500) && retries < maxRetries) {
            retries++;
            await this.sleep(1000 * Math.pow(2, retries));
            continue;
          }

          const text = await res.text().catch(() => "Unknown error");
          throw new ApiError(res.status, text);

        } catch (error) {
          if (timeoutId) clearTimeout(timeoutId);
          if (parentSignal) parentSignal.removeEventListener('abort', abortListener);

          if (error instanceof AuthError || error instanceof ApiError) {
            throw error;
          }
          
          if (error instanceof Error && error.name === 'AbortError') {
             if (parentSignal?.aborted) {
               throw new NetworkError("Request aborted by user");
             }
             
             if (retries < maxRetries) {
               retries++;
               await this.sleep(1000 * Math.pow(2, retries));
               continue;
             }
             throw new NetworkError(`Request timed out after ${this.opts.timeout}ms`);
          }

          if (retries < maxRetries) {
            retries++;
            await this.sleep(1000 * Math.pow(2, retries));
            continue;
          }

          throw new NetworkError(error instanceof Error ? error.message : "Network error or server unreachable");
        }
      }
    };
  }
}
