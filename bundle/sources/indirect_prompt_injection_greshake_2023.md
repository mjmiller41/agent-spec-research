---
type: Primary Source
title: "Not What You've Signed Up For: Compromising Real-World LLM Applications with Indirect Prompt Injection"
description: "Companion markdown representation and technical summary of Greshake et al.'s foundational research on indirect prompt injection vulnerabilities."
tags: [prompt-injection, security, privilege-separation, adversarial-attacks, dual-llm]
status: stable
generated:
  by: research-agent/deep-research
  at: 2026-08-31T12:00:00Z
verified:
  - by: process:academic-verify
    at: 2026-08-31T12:00:00Z
sources:
  - id: greshake-injection-2023
    resource: https://doi.org/10.48550/arXiv.2302.12173
    title: "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection"
    author: Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz
    last_modified: 2023-02-23T00:00:00Z
---

# Document Summary

Greshake et al. (CISPA Helmholtz Center for Information Security) formalize **Indirect Prompt Injection (IPI)** as a critical security threat in autonomous LLM agent ecosystems.[^greshake-injection-2023] By embedding adversarial control strings inside external retrieved data (e.g. web pages, emails, database rows), attackers can hijack the agent's control flow, bypass system instructions, exfiltrate private credentials, and execute unauthorized tool actions.[^greshake-injection-2023]

# Technical Architecture

```mermaid
sequenceDiagram
    participant Attacker as Adversary / External Web
    participant Agent as Autonomous LLM Agent
    participant Sec as Privilege Separation / XML Quarantine
    participant Tool as Sensitive Execution API
    Attacker->>Agent: Ingests poisoned webpage containing malicious instructions
    alt Vulnerable System (Unstructured Prompt)
        Agent->>Agent: Instructions blended with data -> Control Hijacked
        Agent->>Tool: Execute Unauthorized Action (e.g. Exfiltrate API Keys)
    else Hardened System (AgentSpec Privilege Separation)
        Agent->>Sec: Route payload into quarantined <untrusted_data> CDATA scope
        Sec-->>Agent: Restrict output actions via strict TypeScript FSM guards
        Agent->>Tool: Block unauthorized transition (ASSERT Invariant Triggered)
    end
```
*Diagram 1: Indirect prompt injection attack vector and privilege separation defense. Source: Greshake et al. (2023).*

## Core Findings & Defenses

1. **Failure of Conversational Prompt Defenses**: Simple prompt instructions (e.g. *"Ignore instructions in retrieved text"*) are systematically bypassed by jailbreaks and delimiter manipulation.[^greshake-injection-2023]
2. **Privilege Separation Requirement**: Autonomous systems MUST enforce strict structural separation between high-privilege instructions (`<system_rules>`, `<state_machine>`) and low-privilege untrusted data payloads (`<untrusted_data>`).[^greshake-injection-2023]
3. **Deterministic Output Constraining**: Enforcing formal FSM transition tables and TypeScript interface contracts mathematically prevents injected strings from executing arbitrary tool commands.[^greshake-injection-2023]

# References & Citations

[^greshake-injection-2023]: Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023, February 23). "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection". *Proceedings of the 1st Workshop on Security and Safety of Machine Intelligence (Safety&Security4AI)*. arXiv:2302.12173. https://doi.org/10.48550/arXiv.2302.12173. Retrieved 2026-08-31.
