import { HttpTransport } from "../../core/http.js"

export class WorkflowResource {
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  async get(workflowId: string, organizationId: string) {
    return this.http.getFetch()(`${this.base}/journeys/api/v1/workflows/${workflowId}`, {
      method: "GET",
      headers: { "x-organization-id": organizationId },
    }).then(r => r.json())
  }

  async verify(workflowIds: number[], organizationId: string) {
    return this.http.getFetch()(`${this.base}/journeys/api/v1/workflows/verify`, {
      method: "GET",
      headers: {
        "x-organization-id": organizationId,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ workflow_ids: workflowIds }),
    }).then(r => r.json())
  }

  async update(workflowId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/journeys/v1/workflow/${workflowId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }
}
