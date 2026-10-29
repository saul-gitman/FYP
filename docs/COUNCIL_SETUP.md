# Council setup, orchestrator instructions and session memory

Not for council members. Members receive only `COUNCIL_BRIEF.md`.

## 1. Memory carried from the first session (2026-10-29)
- User request: build a simulation tool for the FYP, plan first, then debate the plan with GPT and Qwen through "the council AI" and have them judge it.
- Council members requested: **"6sol" at high effort** and **"Qwen next" at max effort**. These names are the user's; no endpoint, API model ID or key for either is recorded anywhere. Confirm both with the user before the first call.
- Order of work: gather information, write the plan, **debate, revise the plan, then build**. Nothing is built before the debate.
- The first session ran on Claude Opus 5.5 (high effort) and committed `docs/PLAN.md` and `docs/COUNCIL_BRIEF.md`. This session (Sonnet 5.5) revised them to v0.2 against the transcript constraints.
- The handover zip `FYP_Handover_2026-10-29.zip` was uploaded to the first session only and is **not** in this repository or this container. The user wants its whole content under `guide/`; that is pending (see §4).

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
| Handover zip | Not available in this container. Upload it to the session or commit it, then it moves to `guide/`. |

## 5. Evaluation of connecting to `mcp.sammm.net/v1`
Feasible in two ways, and both need action from the user first.
- **As a claude.ai connector (recommended):** fix the `sam` entry's authentication, confirm its URL is `https://mcp.sammm.net/v1`, start a fresh session. Its tools then appear as `mcp__sam__*`. No network change is needed for connector traffic, which goes through Anthropic's MCP proxy; the egress denial above applies to calls made from this container.
- **As a direct MCP server from the container** (for scripts): needs the host allowed in the network policy and a credential in an environment secret.
- Risks to check before sending anything: who operates the endpoint, whether it logs prompts, and whether the council brief (project documents, unpublished) may leave the account. The brief contains no personal data. Verify tool names and schemas after connecting before the first real call, and run one harmless test prompt first.
