"""MCP tools indirection layer.

This module is the single point of import for MCP tool loading across the agent.
Tests patch `mcp_tools.get_mcp_tools` to return mock tools.
Production code calls the actual Agent Gateway SDK via mcp_providers.agw.
"""
from mcp_providers.agw import get_mcp_tools

__all__ = ["get_mcp_tools"]
