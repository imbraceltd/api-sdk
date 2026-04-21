from typing import Any, Dict, List
from ..http import HttpTransport, AsyncHttpTransport


class FileServiceResource:
    def __init__(self, http: HttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    def upload_file(self, file: Any, process: bool = True) -> Dict[str, Any]:
        """Upload a file."""
        params = {} if process else {"process": "false"}
        return self._http.request("POST", f"{self._base}/", files={"file": file}, params=params).json()

    def upload_agent_file(self, agent_id: str, file: Any, is_rag: bool = True) -> Dict[str, Any]:
        """Upload a file for a specific agent."""
        return self._http.request(
            "POST", f"{self._base}/agent",
            data={"agent_id": agent_id, "is_rag": str(is_rag).lower()},
            files={"file": file},
        ).json()

    def extract_file(self, file: Any) -> Dict[str, Any]:
        """Extract/embed a PDF file."""
        return self._http.request("POST", f"{self._base}/extract", files={"file": file}).json()

    def list_files(self, content: bool = True) -> List[Dict[str, Any]]:
        """List all files accessible to the current user."""
        params = {} if content else {"content": "false"}
        return self._http.request("GET", f"{self._base}/", params=params).json()

    def search_files(self, filename: str, content: bool = True) -> List[Dict[str, Any]]:
        """Search files by filename pattern (supports wildcards like *.txt)."""
        params: Dict[str, Any] = {"filename": filename}
        if not content:
            params["content"] = "false"
        return self._http.request("GET", f"{self._base}/search", params=params).json()

    def delete_all_files(self) -> Dict[str, Any]:
        """Delete all files (admin only)."""
        return self._http.request("DELETE", f"{self._base}/all").json()

    def get_file(self, file_id: str) -> Dict[str, Any]:
        """Get file metadata by ID."""
        return self._http.request("GET", f"{self._base}/{file_id}").json()

    def download_file(self, file_id: str, attachment: bool = False) -> Any:
        """Download file binary content."""
        params = {"attachment": "true"} if attachment else {}
        return self._http.request("GET", f"{self._base}/{file_id}/content", params=params)

    def download_file_by_name(self, file_id: str, file_name: str) -> Any:
        """Download file binary content by name."""
        return self._http.request("GET", f"{self._base}/{file_id}/content/{file_name}")

    def get_file_html_content(self, file_id: str) -> Any:
        """Get the HTML-rendered content of a file."""
        return self._http.request("GET", f"{self._base}/{file_id}/content/html")

    def get_file_data_content(self, file_id: str) -> Dict[str, str]:
        """Get the extracted text content of a file."""
        return self._http.request("GET", f"{self._base}/{file_id}/data/content").json()

    def update_file_data_content(self, file_id: str, content: str) -> Dict[str, str]:
        """Update the extracted text content of a file."""
        return self._http.request(
            "POST", f"{self._base}/{file_id}/data/content/update",
            json={"content": content},
        ).json()

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        """Delete a file by ID."""
        return self._http.request("DELETE", f"{self._base}/{file_id}").json()

    def get_public_download_url(self, file_id: str) -> str:
        """Build the public download URL for a file (no auth required)."""
        gateway_base = self._base.replace("/v1/file-service", "")
        return f"{gateway_base}/files/download/{file_id}"


class AsyncFileServiceResource:
    def __init__(self, http: AsyncHttpTransport, base: str):
        self._http = http
        self._base = base.rstrip("/")

    async def upload_file(self, file: Any, process: bool = True) -> Dict[str, Any]:
        """Upload a file."""
        params = {} if process else {"process": "false"}
        res = await self._http.request("POST", f"{self._base}/", files={"file": file}, params=params)
        return res.json()

    async def upload_agent_file(self, agent_id: str, file: Any, is_rag: bool = True) -> Dict[str, Any]:
        """Upload a file for a specific agent."""
        res = await self._http.request(
            "POST", f"{self._base}/agent",
            data={"agent_id": agent_id, "is_rag": str(is_rag).lower()},
            files={"file": file},
        )
        return res.json()

    async def extract_file(self, file: Any) -> Dict[str, Any]:
        """Extract/embed a PDF file."""
        res = await self._http.request("POST", f"{self._base}/extract", files={"file": file})
        return res.json()

    async def list_files(self, content: bool = True) -> List[Dict[str, Any]]:
        """List all files accessible to the current user."""
        params = {} if content else {"content": "false"}
        res = await self._http.request("GET", f"{self._base}/", params=params)
        return res.json()

    async def search_files(self, filename: str, content: bool = True) -> List[Dict[str, Any]]:
        """Search files by filename pattern (supports wildcards like *.txt)."""
        params: Dict[str, Any] = {"filename": filename}
        if not content:
            params["content"] = "false"
        res = await self._http.request("GET", f"{self._base}/search", params=params)
        return res.json()

    async def delete_all_files(self) -> Dict[str, Any]:
        """Delete all files (admin only)."""
        res = await self._http.request("DELETE", f"{self._base}/all")
        return res.json()

    async def get_file(self, file_id: str) -> Dict[str, Any]:
        """Get file metadata by ID."""
        res = await self._http.request("GET", f"{self._base}/{file_id}")
        return res.json()

    async def download_file(self, file_id: str, attachment: bool = False) -> Any:
        """Download file binary content."""
        params = {"attachment": "true"} if attachment else {}
        return await self._http.request("GET", f"{self._base}/{file_id}/content", params=params)

    async def download_file_by_name(self, file_id: str, file_name: str) -> Any:
        """Download file binary content by name."""
        return await self._http.request("GET", f"{self._base}/{file_id}/content/{file_name}")

    async def get_file_html_content(self, file_id: str) -> Any:
        """Get the HTML-rendered content of a file."""
        return await self._http.request("GET", f"{self._base}/{file_id}/content/html")

    async def get_file_data_content(self, file_id: str) -> Dict[str, str]:
        """Get the extracted text content of a file."""
        res = await self._http.request("GET", f"{self._base}/{file_id}/data/content")
        return res.json()

    async def update_file_data_content(self, file_id: str, content: str) -> Dict[str, str]:
        """Update the extracted text content of a file."""
        res = await self._http.request(
            "POST", f"{self._base}/{file_id}/data/content/update",
            json={"content": content},
        )
        return res.json()

    async def delete_file(self, file_id: str) -> Dict[str, Any]:
        """Delete a file by ID."""
        res = await self._http.request("DELETE", f"{self._base}/{file_id}")
        return res.json()

    def get_public_download_url(self, file_id: str) -> str:
        """Build the public download URL for a file (no auth required)."""
        gateway_base = self._base.replace("/v1/file-service", "")
        return f"{gateway_base}/files/download/{file_id}"
