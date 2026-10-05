from enum import IntEnum
from typing import List, Dict, Any, Optional

class PriorityLevel(IntEnum):
    APEX_CORE = 1
    SUPPORTING_BODY = 2
    BASE_ARCHIVE = 3

class InvertedPyramidEngine:
    def __init__(self):
        self.layers: Dict[PriorityLevel, List[Dict[str, Any]]] = {
            PriorityLevel.APEX_CORE: [],
            PriorityLevel.SUPPORTING_BODY: [],
            PriorityLevel.BASE_ARCHIVE: []
        }

    def add_layer_node(
        self, 
        priority: PriorityLevel, 
        title: str, 
        content: Any, 
        verification_ref: Optional[Dict[str, Any]] = None
    ):
        node = {
            "title": title,
            "content": content,
            "verification_provenance": verification_ref or {"status": "UNVERIFIED"}
        }
        self.layers[priority].append(node)

    def CompileSynthesis(self) -> Dict[str, Any]:
        return {
            "architectural_version": "Al-Haqq 1.1 / Inverted Pyramid Engine",
            "tier_1_apex": self.layers[PriorityLevel.APEX_CORE],
            "tier_2_body": self.layers[PriorityLevel.SUPPORTING_BODY],
            "tier_3_archive": self.layers[PriorityLevel.BASE_ARCHIVE]
        }
