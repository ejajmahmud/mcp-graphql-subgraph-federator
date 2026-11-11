"""Core GraphQL Subgraph Federator implementation."""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class SubgraphDef:
    name: str
    endpoint: str
    entities: List[str]
    queries: Dict[str, Dict[str, str]]  # query_name -> {param_name: param_type}

@dataclass
class FederatedTool:
    tool_name: str
    description: str
    subgraph_name: str
    parameters: Dict[str, str]

class SubgraphFederator:
    """Compiles disparate GraphQL subgraph definitions into streamlined MCP tools."""
    
    def __init__(self):
        self.subgraphs: Dict[str, SubgraphDef] = {}
        self.compiled_tools: Dict[str, FederatedTool] = {}

    def register_subgraph(self, sg: SubgraphDef) -> None:
        self.subgraphs[sg.name] = sg
        self._recompile_tools()

    def _recompile_tools(self) -> None:
        tools = {}
        for sg_name, sg in self.subgraphs.items():
            for q_name, params in sg.queries.items():
                tool_name = f"{sg_name}_{q_name}"
                desc = f"Executes federated query '{q_name}' on subgraph '{sg_name}' for entities: {', '.join(sg.entities)}"
                tools[tool_name] = FederatedTool(
                    tool_name=tool_name,
                    description=desc,
                    subgraph_name=sg_name,
                    parameters=params
                )
        self.compiled_tools = tools

    def list_mcp_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t.tool_name,
                "description": t.description,
                "inputSchema": {
                    "type": "object",
                    "properties": {k: {"type": v} for k, v in t.parameters.items()},
                    "required": list(t.parameters.keys())
                }
            }
            for t in self.compiled_tools.values()
        ]
