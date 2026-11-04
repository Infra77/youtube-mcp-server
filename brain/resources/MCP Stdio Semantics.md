---
type: research
status: distilled
author: Codex
reviewed: 2026-10-31
requirements: [SE-2, TQ-3]
source_urls: ["https://docs.spring.io/spring-ai/reference/1.1/api/mcp/mcp-server-boot-starter-docs.html"]
---
# MCP Stdio Semantics
## Question and finding
The MCP host starts a child process and negotiates the protocol. Only protocol messages belong on stdout; diagnostic logging must go to stderr. Use the maintained SDK and test initialize, discovery and invocation.
## Implementation consequence
Use this finding in the linked requirements and the corresponding ADR. Validate behavior with
synthetic examples and retain failures in docs/defects.md. External documentation is distinguished
from client mandates and handbook design choices; no original source author is inferred.
## Open evidence
Human review, actual Google project limits and live account acceptance remain pending.
## Related knowledge
[[Codex Project Boundaries]] · [[CI Fixture Isolation]] · [[Project Map]]
