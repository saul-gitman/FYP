# Council setup, orchestrator instructions and session memory

Not for council members. Members receive only `COUNCIL_BRIEF.md`.

## 1. Memory carried from the first session (2026-10-29)
- User request: build a simulation tool for the FYP, plan first, then debate the plan with GPT and Qwen through "the council AI" and have them judge it.
- Council members (names as given by the user, 2026-10-29, second message): **"gpt 6 sol"** at high effort and **"qwen 3.8 flash Q3xxs"** at max effort. The first session wrote them as "6sol" and "Qwen next". These are the user's labels, not verified model IDs: the exact API identifiers are unknown until the MCP server's tool list or model list shows them. "Q3xxs" looks like a quantisation tag (3-bit, XXS), which would mean a locally hosted quantised model; if so, "max effort" may not be a real setting for it. Do not guess corrections: read the real IDs from the server, then fix this line.
- Order of work: gather information, write the plan, **debate, revise the plan, then build**. Nothing is built before the debate.
- The first session ran on Claude Opus 5.5 (high effort) and committed `docs/PLAN.md` and `docs/COUNCIL_BRIEF.md`. This session (Sonnet 5.5) revised them to v0.2 against the transcript constraints.
- The handover zip `FYP_Handover_2026-10-29.zip` was first uploaded to the first session only. It was re-uploaded to the second session, verified against its own `SHA256SUMS.txt` (all OK, 129 files, no path traversal or symlinks), and its whole content is now under `guide/` (folder contents copied unchanged, without the top-level `FYP_Handover_2026-10-29/` wrapper). `guide/05_References/download_reference_pdfs.py` was not run.

## 2. Orchestrator instructions (for Claude)
1. Send `docs/COUNCIL_BRIEF.md` verbatim to each member as one self-contained message. Add nothing that hints at the preferred answer. Do not send the user's email, session links or credentials.
2. Run **round 1** independently: each member answers the brief and returns the required format (verdict, six scores, top 3 objections with fixes, answers to Q1–10, one cut, one add). Record effort level and model ID per call.
3. Run **round 2 (debate)**: give each member the other's round-1 answer and ask for a rebuttal and a revised verdict. One round only.
4. **Judging:** both members judge the plan, and Claude is judged too: ask them to say where Claude's plan or Claude's handling of their objections is wrong. Claude does not average the scores.
5. Treat council output as advice. Where a member gives a number or equation, check it independently before it goes into the plan. Where members disagree, put both views and the evidence to the user instead of picking silently.
6. Revise `docs/PLAN.md` (v0.3) with a change log mapping each accepted or rejected objection to a reason. Save the raw answers under `docs/council/` with timestamps.
7. Never claim a model answered if the call failed or the tool returned an error. Report the failure.
8. Do not invent material constants. Keep the provenance labels: measured, literature, derived, hypothetical.

## 3. Prompt template per member
Message body: the full text of `docs/COUNCIL_BRIEF.md`. Round 2 adds, after the brief:

> Below is the other reviewer's answer. Rebut what you think is wrong, concede what is right, and give a revised verdict in the same format. Also judge the coding agent's plan and the quality of its handling of objections.

## 4. Connector status and blockers (checked 2026-10-29)
| Item | Finding |
|---|---|
| Built-in `Council of AI` connector | Connected. 47 read-only tools over councilof.ai measurement records. `route` is decide-only ("Nothing is executed, called or charged"). **It cannot send prompts to other models**, so it cannot host the debate. |
| `sam` connector (claude.ai account) | Installed, **`needs_reconnect`**, not loaded in this session. The URL behind it was not visible, so it is not confirmed to be `mcp.sammm.net/v1`. Reconnect at https://claude.ai/customize/connectors, then start a new session (connectors are read at session start). |
| Host `mcp.sammm.net:443` | **Denied by the environment network policy** (proxy returned 403 to CONNECT, logged 2026-10-29T08:42Z). Nothing was sent to it. Add the host under Allowed domains in the environment's Network access settings: https://code.claude.com/docs/en/cloud-environments#network-access |
| Auth for the endpoint | Unknown. Do not paste keys into chat or commit them. Use the connector's auth flow, or an environment secret. |
| Handover zip | Done: contents are in `guide/`. |

## 5. Evaluation of connecting to `mcp.sammm.net/v1`
Feasible in two ways, and both need action from the user first.
- **As a claude.ai connector (recommended):** fix the `sam` entry's authentication, confirm its URL is `https://mcp.sammm.net/v1`, start a fresh session. Its tools then appear as `mcp__sam__*`. No network change is needed for connector traffic, which goes through Anthropic's MCP proxy; the egress denial above applies to calls made from this container.
- **As a direct MCP server from the container** (for scripts): needs the host allowed in the network policy and a credential in an environment secret.
- Risks to check before sending anything: who operates the endpoint, whether it logs prompts, and whether the council brief (project documents, unpublished) may leave the account. The brief contains no personal data. Verify tool names and schemas after connecting before the first real call, and run one harmless test prompt first.

## 6. Diagnostics for whoever is fixing the MCP server (observed 2026-10-29, nothing reached the server)
What was actually observed:
1. **Egress block, not a server error.** From the cloud container, `curl -i https://mcp.sammm.net/v1` fails with `CONNECT tunnel failed, response 403`. The agent proxy log records `connect_rejected ... gateway answered 403 to CONNECT (policy denial or upstream failure)` for `mcp.sammm.net:443` at 2026-10-29T08:42:52Z. This is the environment's allowed-domains policy and says nothing about the server's health. `getent hosts` gave no address in the container, which is expected with proxy-only egress and is not proof the name is missing.
2. **Connector `sam` (id `bc72e9c9-086d-4285-a381-bf4dc961d8e4`)**: `installState: needs_reconnect`, `isAuthless: false`, `customOAuthClientId: null`, `connected: false`, `enabledInChat: false`. So it needs a credential, its stored authorisation is no longer valid, and it was not loaded in either session. It did not appear in the session's "failed to connect" list, so the server was never contacted this session and there is no server-side error text to quote.
3. The connector's URL is not exposed to this agent, so it is not confirmed to be `https://mcp.sammm.net/v1`.

Hypotheses, in order of likelihood (not tested):
- The OAuth grant expired or was revoked, or the refresh failed. Reconnecting in claude.ai connector settings should show the real error text; send that text to the fixing agent.
- The authorisation server does not support dynamic client registration (RFC 7591). The same session shows this exact failure class for another connector: `Incompatible auth server: does not support dynamic client registration`. If `sam` needs a pre-registered client, `customOAuthClientId` (currently null) must be set.
- The server's OAuth metadata is missing or inconsistent: `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server`, or a `401` without a `WWW-Authenticate` header on an unauthenticated request.
- The OAuth redirect URI allow-list lacks claude.ai's callback (`https://claude.ai/api/mcp/auth_callback`; confirm the current value in the connector UI).
- Transport mismatch: the endpoint at `/v1` must answer a JSON-RPC `initialize` POST (streamable HTTP, `Accept: application/json, text/event-stream`), not only SSE or a REST path.

Fast checks for the fixing agent, from a machine with open egress:
```bash
curl -i https://mcp.sammm.net/v1
curl -i https://mcp.sammm.net/.well-known/oauth-protected-resource
curl -i https://mcp.sammm.net/.well-known/oauth-authorization-server
curl -i -X POST https://mcp.sammm.net/v1 -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}'
```
Expect: a `401` with `WWW-Authenticate: Bearer resource_metadata=...` when unauthenticated, valid metadata documents, and a JSON-RPC result (or a clear auth error) for `initialize`. Also check the TLS chain is publicly trusted.
