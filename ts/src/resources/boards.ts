import { HttpTransport } from "../http.js"

export class BoardsResource {
  /**
   * @param base - data-board base URL (gateway/data-board)
   *   Không có version prefix — path trực tiếp.
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  // ─── Boards ──────────────────────────────────────────────────────────────────

  async list(params?: { limit?: number; skip?: number }) {
    const url = new URL(`${this.base}/boards`)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(boardId: string) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}`, { method: "GET" }).then(r => r.json())
  }

  async getByContact(contactId: string) {
    return this.http.getFetch()(`${this.base}/boards/by-contact/${contactId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: { name: string; description?: string }) {
    return this.http.getFetch()(`${this.base}/boards`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(boardId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(boardId: string): Promise<void> {
    await this.http.getFetch()(`${this.base}/boards/${boardId}`, { method: "DELETE" })
  }

  async reorder(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/_order`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async exportCsv(boardId: string, params?: Record<string, string>) {
    const url = new URL(`${this.base}/boards/${boardId}/export_csv`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.text())
  }

  async importCsv(boardId: string, body: FormData) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/import_csv`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async importExcel(boardId: string, body: FormData) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/import_excel`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async getImportProgress(boardId: string) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/import_progress`, { method: "GET" }).then(r => r.json())
  }

  // ─── Fields ──────────────────────────────────────────────────────────────────

  async createField(boardId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/fields`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateField(boardId: string, fieldId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/fields/${fieldId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteField(boardId: string, fieldId: string): Promise<void> {
    await this.http.getFetch()(`${this.base}/boards/${boardId}/fields/${fieldId}`, { method: "DELETE" })
  }

  async reorderFields(boardId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/fields/reorder`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async bulkUpdateFields(boardId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/fields/bulk`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Items (records) ─────────────────────────────────────────────────────────

  async listItems(boardId: string, params?: { limit?: number; skip?: number }) {
    const url = new URL(`${this.base}/boards/${boardId}/items`)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getItem(boardId: string, itemId: string) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}`, { method: "GET" }).then(r => r.json())
  }

  async createItem(boardId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateItem(boardId: string, itemId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteItem(boardId: string, itemId: string): Promise<void> {
    await this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}`, { method: "DELETE" })
  }

  async bulkDeleteItems(boardId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/bulk-delete`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async checkConflict(boardId: string, itemId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}/_is_conflicted`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getRelatedItems(boardId: string, itemId: string, relatedBoardId: string) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}/related/${relatedBoardId}`, { method: "GET" }).then(r => r.json())
  }

  async linkItems(boardId: string, itemId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}/related`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async unlinkItems(boardId: string, itemId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}/related`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Search ──────────────────────────────────────────────────────────────────

  async search(boardId: string, body: { q?: string; limit?: number; offset?: number }) {
    return this.http.getFetch()(`${this.base}/search/${boardId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Segmentation ────────────────────────────────────────────────────────────

  async listSegments(boardId: string) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/segmentation`, { method: "GET" }).then(r => r.json())
  }

  async createSegment(boardId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/segmentation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateSegment(boardId: string, segmentId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/segmentation/${segmentId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteSegment(boardId: string, segmentId: string): Promise<void> {
    await this.http.getFetch()(`${this.base}/boards/${boardId}/segmentation/${segmentId}`, { method: "DELETE" })
  }

  // ─── Knowledge Hub (folders/files via data-board) ────────────────────────────

  async searchFolders(params: { organizationId: string; q?: string }) {
    const url = new URL(`${this.base}/folders/search`)
    url.searchParams.set("organization_id", params.organizationId)
    if (params.q) url.searchParams.set("q", params.q)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getFolder(folderId: string, params?: { recursive?: boolean }) {
    const url = new URL(`${this.base}/folders/${folderId}`)
    if (params?.recursive !== undefined) url.searchParams.set("recursive", String(params.recursive))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async createFolder(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/folders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateFolder(folderId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/folders/${folderId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteFolders(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/folders/delete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async searchFiles(params: { folderId: string }) {
    const url = new URL(`${this.base}/files/search`)
    url.searchParams.set("folder_id", params.folderId)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getFile(fileId: string) {
    return this.http.getFetch()(`${this.base}/files/${fileId}`, { method: "GET" }).then(r => r.json())
  }

  async createFile(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/files`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async uploadFile(body: FormData) {
    return this.http.getFetch()(`${this.base}/files/upload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async downloadFile(fileId: string) {
    return this.http.getFetch()(`${this.base}/files/${fileId}/download`, { method: "GET" })
  }

  async deleteFiles(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/files/delete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async generateAiTags(body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/ai/tag-generation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getLinkPreview(url: string) {
    return this.http.getFetch()(`${this.base}/link_preview/getWebsiteInfo`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    }).then(r => r.json())
  }

  // ─── Board file upload ───────────────────────────────────────────────────────

  async uploadBoardFile(body: FormData) {
    return this.http.getFetch()(`${this.base}/boards/_fileupload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  // ─── Folder contents ─────────────────────────────────────────────────────────

  async getFolderContents(folderId: string) {
    return this.http.getFetch()(`${this.base}/folders/${folderId}/contents`, { method: "GET" }).then(r => r.json())
  }

  // ─── File update ─────────────────────────────────────────────────────────────

  async updateFile(fileId: string, body: Record<string, unknown>) {
    return this.http.getFetch()(`${this.base}/files/${fileId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── External Drive integration ──────────────────────────────────────────────

  async initiateDriveAuth(type: string) {
    return this.http.getFetch()(`${this.base}/auth/${type}/initiate`, { method: "GET" }).then(r => r.json())
  }

  async listDriveFolders(type: string, params?: Record<string, string>) {
    const url = new URL(`${this.base}/${type}/folders`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listDriveFiles(type: string, params?: Record<string, string>) {
    const url = new URL(`${this.base}/${type}/files`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async downloadDriveFile(type: string, params?: Record<string, string>) {
    const url = new URL(`${this.base}/${type}/files/download`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" })
  }

  async getOneDriveSessionStatus() {
    return this.http.getFetch()(`${this.base}/auth/onedrive/files/session/status`, { method: "GET" }).then(r => r.json())
  }
}
