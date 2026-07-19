from pydantic import BaseModel, Field

class SubjectCreate(BaseModel):
    name: str
    code: str
    description: str
    category: str

class SubjectUpdate(BaseModel):
    name: str
    code: str
    description: str
    category: str

class SyllabusCreate(BaseModel):
    subject_id: str
    name: str
    version: str
    description: str

class SyllabusUpdate(BaseModel):
    name: str
    version: str
    description: str

class ModuleCreate(BaseModel):
    syllabus_id: str
    name: str
    order: int
    description: str

class ModuleUpdate(BaseModel):
    name: str
    order: int
    description: str

class TopicCreate(BaseModel):
    module_id: str
    name: str
    order: int
    description: str

class TopicUpdate(BaseModel):
    name: str
    order: int
    description: str
