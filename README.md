OfficeOS Prefect Backend PRD
1. Project Summary

This backend powers a hackathon demo for OfficeOS, a conceptual operating system for managing AI-powered business departments. The full OfficeOS product includes a visual frontend where departments such as Legal, Sales, Finance, and Operations are represented as office spaces and agent teams. For this hackathon submission, the backend scope is intentionally narrow.

The backend will implement one high-clarity Prefect-orchestrated workflow that demonstrates how a department request can trigger a multi-step AI process behind the scenes.

The chosen workflow is a Legal Research Workflow.

The backend will expose a simple API endpoint that the frontend can call. That endpoint will run a Prefect flow, orchestrate several clearly named agent tasks, and return a short legal briefing summary. The implementation should prioritize:

clear orchestration

a visually understandable Prefect graph

strong task naming

useful logs for demo recording

minimal complexity

reliable deployment on Render

This is a hackathon demo backend, not a production system.

2. Goal

Build a small Python backend using FastAPI + Prefect that demonstrates:

a frontend-triggered legal research request

a multi-step Prefect workflow

clearly named agent-style tasks

detailed logs that show the agents “doing work”

a final legal briefing returned through the API

a Prefect run graph that looks clean and understandable in a short demo video

3. Primary Use Case

A user in OfficeOS requests legal research on a supplier contract issue.

Example topic:

Legal risks of supplier contracts for a hardware startup

The backend receives that request through an API endpoint, runs a Prefect flow, performs several AI-assisted task steps, and returns a concise legal briefing.

This workflow is also intended to be shown in the Prefect UI during the demo video.

4. In Scope

The backend should include:

Python project structure

FastAPI server

one API endpoint for legal research

one Prefect flow called by that endpoint

multiple Prefect tasks with clear “agent” naming

OpenAI integration via environment variable

.env support for local development

Render-friendly deployment setup

detailed task logging

final structured legal briefing output

5. Out of Scope

Do not implement:

authentication

database

user accounts

persistent storage

background queues beyond Prefect flow execution

websocket updates

frontend implementation

multi-workflow platform

scheduling system

retries beyond basic defaults unless trivial

complex state management

multi-tenant design

production security hardening beyond normal basics

This should remain a single-request, single-workflow demo backend.

6. Tech Stack

The backend must use:

Python

FastAPI

Prefect

OpenAI API

python-dotenv or equivalent for local .env loading

Deployment target:

Render

7. Architecture Overview

The architecture should be simple:

Frontend
→ POST /api/legal-research
→ FastAPI endpoint
→ Prefect flow execution
→ multiple agent tasks
→ final legal briefing returned as JSON

The FastAPI application and the Prefect flow should live in the same backend service for simplicity.

No separate worker infrastructure is required for this hackathon implementation unless absolutely necessary.

8. API Contract
Endpoint

POST /api/legal-research

Request Body
{
  "topic": "Legal risks of supplier contracts for a hardware startup"
}
Request Model

The request should minimally contain:

topic: string

A Pydantic request model should be used.

Response Body
{
  "status": "completed",
  "topic": "Legal risks of supplier contracts for a hardware startup",
  "summary": "Short legal briefing text..."
}
Response Model

The response should minimally contain:

status: string

topic: string

summary: string

Optional additional fields are allowed only if they do not clutter the implementation. Keep it simple.

9. Workflow Design
Flow Name

Use a clear flow name:

legal_research_flow

This name should appear cleanly in Prefect UI.

High-Level Workflow Shape

Implement the workflow in a way that is initially reliable and simple. Sequential execution is acceptable for the first implementation. The structure should still preserve the conceptual shape of specialized agents.

Preferred conceptual workflow:

prepare_query_agent

research_agent

risk_assessment_agent

precedent_search_agent

legal_reasoning_agent

briefing_agent

If time permits, research_agent, risk_assessment_agent, and precedent_search_agent may be upgraded to run in parallel after prepare_query_agent. However, the first implementation should prioritize correctness and reliability over concurrency.

Recommended Initial Sequential Flow
legal_research_flow
    ↓
prepare_query_agent
    ↓
research_agent
    ↓
risk_assessment_agent
    ↓
precedent_search_agent
    ↓
legal_reasoning_agent
    ↓
briefing_agent
Optional Later Parallel Upgrade

If easy to implement later, the middle three tasks can branch from the same prepared query and merge into the reasoning step.

10. Agent Task Responsibilities

Each task should have a distinct purpose and a distinct prompt style so the logs and outputs feel like multiple agents working together.

10.1 prepare_query_agent

Purpose:

normalize and structure the incoming topic

convert the user topic into a clean legal research prompt

identify the research focus

Input:

original topic string

Output:

prepared research query string

10.2 research_agent

Purpose:

produce high-level legal research context

identify the major legal themes related to the topic

generate a concise research foundation

Input:

prepared query

Output:

legal research notes

10.3 risk_assessment_agent

Purpose:

identify likely risks and liabilities

focus on practical business exposure

surface areas that may create problems for a startup

Input:

prepared query, or research notes if sequential

Output:

risk assessment notes

10.4 precedent_search_agent

Purpose:

identify analogous legal or business scenarios

produce example situations or precedent-style guidance

this does not need to cite real cases unless easy; synthetic but plausible guidance is acceptable for hackathon purposes

Input:

prepared query, or risk/research notes if sequential

Output:

precedent-style notes

10.5 legal_reasoning_agent

Purpose:

synthesize the previous task outputs

reason about implications

translate agent findings into a coherent legal interpretation

Input:

outputs from research, risk, and precedent tasks

Output:

combined reasoning text

10.6 briefing_agent

Purpose:

produce a concise final business-facing briefing

output should be readable in the frontend and useful in the demo

Input:

legal reasoning output

Output:

short legal briefing summary

11. Final Output Format

The final summary returned by the API should be clearly structured and easy to read in a demo.

Preferred format:

Key Issue:
...

Potential Risk:
...

Recommended Action:
...

Do not return a wall of text unless absolutely necessary.

The final output should feel like something a founder or department head could quickly skim.

12. OpenAI Integration

The backend should use the OpenAI API for task generation.

Requirements

Read API key from environment variable

Do not hardcode credentials

Use .env for local development

Use Render environment variables in deployment

.env must be included in .gitignore

The repository must not require committing secrets

Environment Variable

Use:

OPENAI_API_KEY

Optional:

OPENAI_MODEL may also be supported for flexibility

Fallback Behavior

If OPENAI_API_KEY is missing, the system may either:

return a clean configuration error, or

optionally fall back to mocked output if that is faster for demo resilience

Best default:

return a clear error message unless fallback is trivial to implement

13. Logging Requirements

Detailed logging is required because the Prefect logs are part of the demo value.

Each task should log clearly what it is doing.

Example style:

[Prepare Query Agent] Structuring legal research topic

[Research Agent] Gathering legal context

[Risk Assessment Agent] Evaluating potential liabilities

[Precedent Search Agent] Searching similar scenarios

[Legal Reasoning Agent] Synthesizing legal implications

[Briefing Agent] Generating executive legal briefing

The logs should make the workflow feel like a team of specialized agents.

Avoid vague logs like “starting task” or “processing.”

14. Prefect Visualization Requirements

The Prefect UI should look intentional and readable.

Requirements

use clear flow name

use clear task names

tasks should appear as distinct steps

graph should be understandable at a glance

avoid giant monolithic task functions

preserve agent-like naming

The visual goal is for a viewer to immediately understand:

a legal request came in

several specialized agents worked on it

their results were synthesized

a briefing was produced

15. FastAPI Requirements

The FastAPI app should be simple and clean.

Requirements

include a root health endpoint if convenient, such as /health

include the main legal research endpoint

validate request/response with Pydantic models

return clean JSON

use standard error handling

keep implementation minimal and readable

The server should be able to run locally with a command like:

uvicorn main:app --reload

or equivalent app entrypoint.

16. Error Handling

Use simple, clear error handling.

Requirements:

wrap flow execution in try/except

return HTTP errors with readable messages

if OpenAI configuration is missing, return a clear setup error

if flow execution fails, return a concise failure message

Example error response:

{
  "status": "error",
  "message": "Legal research workflow failed"
}

No elaborate recovery logic is needed.

17. Project Structure Recommendations

A simple project layout is preferred.

Example:

backend/
  app/
    main.py
    flows/
      legal_research.py
    models/
      schemas.py
    services/
      openai_client.py
  requirements.txt
  render.yaml (optional)
  .env.example
  README.md

Exact structure may vary, but keep it clean and unsurprising.

18. Deployment Requirements for Render

The backend should be deployable on Render with minimal friction.

Requirements:

Python service

install dependencies from requirements.txt

start command clearly documented

environment variables documented

no local-only assumptions

.env.example included for developer setup

Document at least:

OPENAI_API_KEY

optional OPENAI_MODEL

19. Demo-Oriented Priorities

This project is intended for a short hackathon video.

Therefore prioritize:

Prefect graph clarity

flow reliability

clean task naming

detailed logs

a readable final summary

easy local and Render deployment

Do not prioritize production features.

20. Success Criteria

The backend is successful if:

POST /api/legal-research works

the Prefect flow runs successfully

the Prefect UI shows a clean multi-step workflow

each task logs meaningful activity

the API returns a short structured legal briefing

the service can run locally and deploy on Render

OpenAI API key is read securely from environment variables

21. Implementation Guidance

The coding agent should optimize for:

speed of implementation

readability

demo reliability

simple deployment

visually satisfying orchestration

If there is a tradeoff between sophistication and reliability, choose reliability.

Sequential orchestration is acceptable for the first implementation. If the initial version works and time remains, upgrading the middle task group to parallel execution is a bonus.

22. One-Sentence Summary

Build a FastAPI + Prefect backend that exposes a single legal research endpoint, orchestrates several clearly named AI agent tasks using OpenAI, logs each step clearly, and returns a concise legal briefing suitable for a hackathon demo and Prefect visualization.
