import { TokenManager } from "./auth/token-manager.js";
import { AuthError, ApiError, NetworkError } from "./errors.js";

interface TransportOptions {
  apiKey?: string;
  timeout: number;
  tokenManager: TokenManager;
}

export class HttpTransport {
  constructor(private readonly opts: TransportOptions) {}

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
        if (this.opts.apiKey) {
          headers.set("x-access-token", this.opts.apiKey);
        }

        const token = this.opts.tokenManager.getToken();
        if (token) {
          headers.set("authorization", `Bearer ${token}`);
        }

        try {
          const res = await globalThis.fetch(input, reqInit);
          
          if (timeoutId) clearTimeout(timeoutId);
          if (parentSignal) parentSignal.removeEventListener('abort', abortListener);

          if (res.ok) {
            return res;
          }

          if (res.status === 401 || res.status === 403) {
            throw new AuthError("Invalid or expired access token.");
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
