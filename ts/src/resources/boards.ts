import { HttpTransport } from "../http.js"
import type { Board, BoardItem, PagedResponse } from "../types/index.js"

// ─── Board update / reorder interfaces ───────────────────────────────────────

export interface UpdateBoardInput {
  name?: string
  description?: string
  [key: string]: unknown
}

export interface ReorderBoardsInput {
  order: string[]
  [key: string]: unknown
}

export interface ReorderBoardsResponse {
  success: boolean
  [key: string]: unknown
}

export interface ImportResponse {
  success: boolean
  imported?: number
  errors?: unknown[]
  [key: string]: unknown
}

export interface ImportProgressResponse {
  status: string
  progress?: number
  total?: number
  [key: string]: unknown
}

// ─── Field interfaces ─────────────────────────────────────────────────────────

export interface BoardField {
  _id: string
  name: string
  type: string
  options?: unknown[]
  required?: boolean
  [key: string]: unknown
}

export interface CreateFieldInput {
  name: string
  type: string
  options?: unknown[]
  required?: boolean
  [key: string]: unknown
}

export interface UpdateFieldInput {
  name?: string
  options?: unknown[]
  required?: boolean
  [key: string]: unknown
}

export interface ReorderFieldsInput {
  field_ids: string[]
  [key: string]: unknown
}

export interface BulkUpdateFieldsInput {
  fields: Partial<BoardField>[]
  [key: string]: unknown
}

export interface FieldOperationResponse {
  success: boolean
  field?: BoardField
  [key: string]: unknown
}

// ─── Item interfaces ─────────────────────────────────────────────────────────

export interface CreateItemInput {
  [key: string]: unknown
}

export interface UpdateItemInput {
  [key: string]: unknown
}

export interface BulkDeleteItemsInput {
  item_ids: string[]
  [key: string]: unknown
}

export interface BulkDeleteItemsResponse {
  success: boolean
  deleted?: number
  [key: string]: unknown
}

export interface CheckConflictInput {
  version?: number
  [key: string]: unknown
}

export interface LinkItemsInput {
  related_board_id: string
  related_item_ids: string[]
  [key: string]: unknown
}

export interface LinkItemsResponse {
  success: boolean
  [key: string]: unknown
}

// ─── Segment interfaces ───────────────────────────────────────────────────────

export interface BoardSegment {
  _id: string
  name: string
  filter?: Record<string, unknown>
  [key: string]: unknown
}

export interface CreateSegmentInput {
  name: string
  filter?: Record<string, unknown>
  [key: string]: unknown
}

export interface UpdateSegmentInput {
  name?: string
  filter?: Record<string, unknown>
  [key: string]: unknown
}

// ─── Folder interfaces ────────────────────────────────────────────────────────

export interface KnowledgeFolder {
  _id: string
  name: string
  organization_id?: string
  parent_id?: string
  [key: string]: unknown
}

export interface CreateFolderInput {
  name: string
  organization_id?: string
  parent_id?: string
  [key: string]: unknown
}

export interface UpdateFolderInput {
  name?: string
  [key: string]: unknown
}

export interface DeleteFoldersInput {
  folder_ids: string[]
  [key: string]: unknown
}

export interface DeleteFoldersResponse {
  success: boolean
  deleted?: number
  [key: string]: unknown
}

// ─── File interfaces ──────────────────────────────────────────────────────────

export interface KnowledgeFile {
  _id: string
  name: string
  folder_id?: string
  url?: string
  size?: number
  [key: string]: unknown
}

export interface CreateFileInput {
  name: string
  folder_id?: string
  content?: string
  [key: string]: unknown
}

export interface UpdateFileInput {
  name?: string
  content?: string
  [key: string]: unknown
}

export interface DeleteFilesInput {
  file_ids: string[]
  [key: string]: unknown
}

export interface DeleteFilesResponse {
  success: boolean
  deleted?: number
  [key: string]: unknown
}

export interface UploadFileResponse {
  url: string
  file_id?: string
  [key: string]: unknown
}

export interface AiTagsInput {
  file_id?: string
  text?: string
  [key: string]: unknown
}

export interface AiTagsResponse {
  tags: string[]
  [key: string]: unknown
}

export interface LinkPreviewResponse {
  title?: string
  description?: string
  image?: string
  url: string
  [key: string]: unknown
}

// ─── Drive interfaces ─────────────────────────────────────────────────────────

export interface DriveAuthResponse {
  auth_url?: string
  [key: string]: unknown
}

export interface DriveItem {
  id: string
  name: string
  [key: string]: unknown
}

export interface OneDriveSessionStatus {
  status: string
  [key: string]: unknown
}

export class BoardsResource {
  /**
   * @param base - data-board base URL (gateway/data-board)
   *   No version prefix — path is used directly.
   */
  constructor(private readonly http: HttpTransport, private readonly base: string) {}

  // ─── Boards ──────────────────────────────────────────────────────────────────

  async list(params?: { limit?: number; skip?: number }): Promise<{ data: Board[] }> {
    const url = new URL(`${this.base}/boards`)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async get(boardId: string): Promise<Board> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}`, { method: "GET" }).then(r => r.json())
  }

  async getByContact(contactId: string): Promise<Board> {
    return this.http.getFetch()(`${this.base}/boards/by-contact/${contactId}`, { method: "GET" }).then(r => r.json())
  }

  async create(body: { name: string; description?: string }): Promise<Board> {
    return this.http.getFetch()(`${this.base}/boards`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async update(boardId: string, body: UpdateBoardInput): Promise<Board> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async delete(boardId: string): Promise<void> {
    await this.http.getFetch()(`${this.base}/boards/${boardId}`, { method: "DELETE" })
  }

  async reorder(body: ReorderBoardsInput): Promise<ReorderBoardsResponse> {
    return this.http.getFetch()(`${this.base}/boards/_order`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async exportCsv(boardId: string, params?: Record<string, string>): Promise<string> {
    const url = new URL(`${this.base}/boards/${boardId}/export_csv`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.text())
  }

  async importCsv(boardId: string, body: FormData): Promise<ImportResponse> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/import_csv`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async importExcel(boardId: string, body: FormData): Promise<ImportResponse> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/import_excel`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async getImportProgress(boardId: string): Promise<ImportProgressResponse> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/import_progress`, { method: "GET" }).then(r => r.json())
  }

  // ─── Fields ──────────────────────────────────────────────────────────────────

  async createField(boardId: string, body: CreateFieldInput): Promise<BoardField> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/fields`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateField(boardId: string, fieldId: string, body: UpdateFieldInput): Promise<BoardField> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/fields/${fieldId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteField(boardId: string, fieldId: string): Promise<void> {
    await this.http.getFetch()(`${this.base}/boards/${boardId}/fields/${fieldId}`, { method: "DELETE" })
  }

  async reorderFields(boardId: string, body: ReorderFieldsInput): Promise<FieldOperationResponse> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/fields/reorder`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async bulkUpdateFields(boardId: string, body: BulkUpdateFieldsInput): Promise<FieldOperationResponse> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/fields/bulk`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Items (records) ─────────────────────────────────────────────────────────

  async listItems(boardId: string, params?: { limit?: number; skip?: number }): Promise<PagedResponse<BoardItem>> {
    const url = new URL(`${this.base}/boards/${boardId}/items`)
    if (params?.limit)  url.searchParams.set("limit", String(params.limit))
    if (params?.skip !== undefined) url.searchParams.set("skip", String(params.skip))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getItem(boardId: string, itemId: string): Promise<BoardItem> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}`, { method: "GET" }).then(r => r.json())
  }

  async createItem(boardId: string, body: CreateItemInput): Promise<BoardItem> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateItem(boardId: string, itemId: string, body: UpdateItemInput): Promise<BoardItem> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteItem(boardId: string, itemId: string): Promise<void> {
    await this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}`, { method: "DELETE" })
  }

  async bulkDeleteItems(boardId: string, body: BulkDeleteItemsInput): Promise<BulkDeleteItemsResponse> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/bulk-delete`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async checkConflict(boardId: string, itemId: string, body: CheckConflictInput): Promise<{ is_conflicted: boolean }> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}/_is_conflicted`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getRelatedItems(boardId: string, itemId: string, relatedBoardId: string): Promise<BoardItem[]> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}/related/${relatedBoardId}`, { method: "GET" }).then(r => r.json())
  }

  async linkItems(boardId: string, itemId: string, body: LinkItemsInput): Promise<LinkItemsResponse> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}/related`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async unlinkItems(boardId: string, itemId: string, body: LinkItemsInput): Promise<LinkItemsResponse> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/items/${itemId}/related`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Search ──────────────────────────────────────────────────────────────────

  async search(boardId: string, body: { q?: string; limit?: number; offset?: number }): Promise<PagedResponse<BoardItem>> {
    return this.http.getFetch()(`${this.base}/search/${boardId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── Segmentation ────────────────────────────────────────────────────────────

  async listSegments(boardId: string): Promise<BoardSegment[]> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/segmentation`, { method: "GET" }).then(r => r.json())
  }

  async createSegment(boardId: string, body: CreateSegmentInput): Promise<BoardSegment> {
    return this.http.getFetch()(`${this.base}/boards/${boardId}/segmentation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateSegment(boardId: string, segmentId: string, body: UpdateSegmentInput): Promise<BoardSegment> {
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

  async searchFolders(params: { organizationId: string; q?: string }): Promise<KnowledgeFolder[]> {
    const url = new URL(`${this.base}/folders/search`)
    url.searchParams.set("organization_id", params.organizationId)
    if (params.q) url.searchParams.set("q", params.q)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getFolder(folderId: string, params?: { recursive?: boolean }): Promise<KnowledgeFolder> {
    const url = new URL(`${this.base}/folders/${folderId}`)
    if (params?.recursive !== undefined) url.searchParams.set("recursive", String(params.recursive))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async createFolder(body: CreateFolderInput): Promise<KnowledgeFolder> {
    return this.http.getFetch()(`${this.base}/folders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async updateFolder(folderId: string, body: UpdateFolderInput): Promise<KnowledgeFolder> {
    return this.http.getFetch()(`${this.base}/folders/${folderId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async deleteFolders(body: DeleteFoldersInput): Promise<DeleteFoldersResponse> {
    return this.http.getFetch()(`${this.base}/folders/delete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async searchFiles(params: { folderId: string }): Promise<KnowledgeFile[]> {
    const url = new URL(`${this.base}/files/search`)
    url.searchParams.set("folder_id", params.folderId)
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async getFile(fileId: string): Promise<KnowledgeFile> {
    return this.http.getFetch()(`${this.base}/files/${fileId}`, { method: "GET" }).then(r => r.json())
  }

  async createFile(body: CreateFileInput): Promise<KnowledgeFile> {
    return this.http.getFetch()(`${this.base}/files`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async uploadFile(body: FormData): Promise<UploadFileResponse> {
    return this.http.getFetch()(`${this.base}/files/upload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  async downloadFile(fileId: string): Promise<Response> {
    return this.http.getFetch()(`${this.base}/files/${fileId}/download`, { method: "GET" })
  }

  async deleteFiles(body: DeleteFilesInput): Promise<DeleteFilesResponse> {
    return this.http.getFetch()(`${this.base}/files/delete`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async generateAiTags(body: AiTagsInput): Promise<AiTagsResponse> {
    return this.http.getFetch()(`${this.base}/ai/tag-generation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  async getLinkPreview(url: string): Promise<LinkPreviewResponse> {
    return this.http.getFetch()(`${this.base}/link_preview/getWebsiteInfo`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    }).then(r => r.json())
  }

  // ─── Board file upload ───────────────────────────────────────────────────────

  async uploadBoardFile(body: FormData): Promise<{ url: string }> {
    return this.http.getFetch()(`${this.base}/boards/_fileupload`, {
      method: "POST",
      body,
    }).then(r => r.json())
  }

  // ─── Folder contents ─────────────────────────────────────────────────────────

  async getFolderContents(folderId: string): Promise<KnowledgeFolder> {
    return this.http.getFetch()(`${this.base}/folders/${folderId}/contents`, { method: "GET" }).then(r => r.json())
  }

  // ─── File update ─────────────────────────────────────────────────────────────

  async updateFile(fileId: string, body: UpdateFileInput): Promise<KnowledgeFile> {
    return this.http.getFetch()(`${this.base}/files/${fileId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(r => r.json())
  }

  // ─── External Drive integration ──────────────────────────────────────────────

  async initiateDriveAuth(type: string): Promise<DriveAuthResponse> {
    return this.http.getFetch()(`${this.base}/auth/${type}/initiate`, { method: "GET" }).then(r => r.json())
  }

  async listDriveFolders(type: string, params?: Record<string, string>): Promise<DriveItem[]> {
    const url = new URL(`${this.base}/${type}/folders`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async listDriveFiles(type: string, params?: Record<string, string>): Promise<DriveItem[]> {
    const url = new URL(`${this.base}/${type}/files`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" }).then(r => r.json())
  }

  async downloadDriveFile(type: string, params?: Record<string, string>): Promise<Response> {
    const url = new URL(`${this.base}/${type}/files/download`)
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v))
    return this.http.getFetch()(url, { method: "GET" })
  }

  async getOneDriveSessionStatus(): Promise<OneDriveSessionStatus> {
    return this.http.getFetch()(`${this.base}/auth/onedrive/files/session/status`, { method: "GET" }).then(r => r.json())
  }
}
