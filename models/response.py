from typing import Optional, Any
from pydantic import BaseModel

class LinkResponse(BaseModel):
    """Link Response Object - Содержит URL ресурса."""
    href: str
    method: str
    templated: Optional[bool] = None

class LinkUploadResponse(BaseModel):
    """LinkUpload Response Object - Содержит URL для загрузки ресурса."""
    operation_id: int
    href: str
    method: str
    templated: Optional[bool] = None

class ResourceResponse(BaseModel):
    """Resource Response Onject - Содержит описание ресурса, мета-информация о файле или папке."""
    path: str
    type: str
    name: str
    created: str
    modified: str
    size: Optional[int] = None
    mime_type: Optional[str] = None
    md5: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error Response Object - Содержит идентификатор, сообщение и описание ошибки"""
    error: str
    description: str
    message: str
    details: Optional[Any] = None

class DeleteResourceResponse(BaseModel):
    """DeleteResource Response Object - Содержит URL ресурса."""
    href: Optional[str] = None
    method: Optional[str] = None
    templated: Optional[bool] = None
