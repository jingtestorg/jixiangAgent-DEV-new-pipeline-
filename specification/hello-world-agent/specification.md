# Specification: hello-world-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read the project input (`product-requirements-document.md`, `intent.md`)
- [x] Bootstrap agent code in `assets/hello-world-agent/` using instructions from the sap-agent-bootstrap section (invoke from inside `assets/hello-world-agent/`, use copy commands — do NOT create files manually)
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

No runtime skills required — the response logic is a static "hello world" message with no branching logic or domain-specific knowledge.

---

## Project-Specific Tasks

## Hello World Response

- [x] Open `assets/hello-world-agent/app/agent.py`
- [x] In the agent's `stream()` method (or equivalent handler), ensure the agent responds with exactly `"hello world"` to any incoming user message, regardless of content
- [x] Update the system prompt (`get_system_prompt()`) to instruct the agent: "You are a hello world agent. For every user message, respond with exactly: hello world"
- [x] Confirm the agent card at `/.well-known/agent.json` reflects the correct name and description for the hello world agent

## Response Latency

- [x] Verify the agent response is generated in-memory without unnecessary delays (no external API calls, no wait logic)
- [x] Manually time a local request to confirm response time is consistently under 2 seconds

---

## Business Instrumentation

- [x] Implement business step instrumentation for each milestone from the PRD: structured logging with pattern `[MILESTONE_ID].[achieved|missed]: [description]` and OpenTelemetry custom spans. See [guidelines-agent-python.md](../guidelines-agent-python.md) for Python-specific implementation.

  Required milestone log statements:
  - `M1.achieved: agent project scaffolded successfully` / `M1.missed: agent scaffolding failed or incomplete`
  - `M2.achieved: hello world response logic implemented and verified` / `M2.missed: agent did not return expected hello world response`
  - `M3.achieved: all tests passed` / `M3.missed: one or more tests failed`
  - `M4.achieved: agent deployed and responding within latency target` / `M4.missed: deployment failed or latency target not met`

- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

No SAP API or MCP server integration required — the agent responds with a static message.

- [x] Skip all MCP-related tasks (no `api-specs/`, no `mcp-specs/`, no `mcp-mock.json` needed)

---

## Testing

- [x] `conftest.py` only sets `IBD_TESTING=true`
- [x] Write one unit test in `assets/hello-world-agent/tests/` that sends a message to the agent and asserts the response contains "hello world"
- [x] Write one integration test calling the agent's `invoke` function end-to-end with a mocked LLM that returns "hello world"
- [x] Run `pytest` from `assets/hello-world-agent/` (no args) — coverage must be ≥ 70% (77% achieved)
- [x] Run `pytest` again from `assets/hello-world-agent/` (no args) to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/hello-world-agent/`
