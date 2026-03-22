from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class Incident(str, Enum):
    DETECTED = "detected"
    INVESTIGATING = "investigating"
    PROPOSED = "proposed"
    REMEDIATED = "remediated"
    FAILED = "failed"


class IncidentContext(BaseModel):
    incident_id: str
    service_name: str
    severity: str
    metrics: Dict[str, float] = Field(default_factory=dict)
    logs: List[str] = Field(default_factory=list)
    trace_ids: List[str] = Field(default_factory=list)
    status: IncidentStatus = IncidentStatus.DETECTED
    timestamp: datetime = Field(default_factory=datetime.now)


class AgentAction(BaseModel):
    tool_name: str
    arguments: Dict
    reasoning: str

