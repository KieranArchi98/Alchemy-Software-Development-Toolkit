ALCHEMY
AI-ASSISTED SOFTWARE DESIGN & MVP BOOTSTRAPPING PLATFORM
PROJECT SPECIFICATION (PLAIN TEXT)

OVERVIEW

Alchemy is an AI-driven software design and planning application that helps users take an idea from an undefined concept to a fully specified, AI-ready MVP implementation plan.

The core goal of Alchemy is to eliminate architectural blind spots, missing requirements, and poorly defined foundations by guiding users through a structured, exhaustive design process before any code is written.

Alchemy does not build software directly. Instead, it produces:

A complete project specification

A canonical machine-readable context (JSON)

A phased implementation roadmap with checklists

A sequential list of AI prompts that can be handed to any AI IDE (e.g. Cursor, Replit, Windsurf) to bootstrap an MVP

Alchemy is tool-agnostic, stack-agnostic, and AI-IDE-agnostic.

TARGET USERS

Alchemy is intended for:

Developers

Founders

Technical learners

Non-technical users with ideas

Anyone using AI to build software

The system is designed to work even if the user:

Does not know what technologies to choose

Does not know which questions to ask

Does not know how to architect frontend or backend systems

In these cases, Alchemy provides AI-recommended defaults that follow industry standards.

CORE PRINCIPLES

JSON is the single source of truth

Human-readable documentation is derived from JSON

Prompts are derived from the roadmap

The user can override any decision at any time

Recent decisions override earlier ones

AI defaults exist for every decision

Frontend UI is stable and not redesigned unnecessarily

The system must be deterministic and replayable

HIGH-LEVEL FUNCTIONALITY

Alchemy provides a workspace where users:

Enter an initial idea

Answer a guided sequence of design questions

Receive AI-recommended options where unsure

See their project specification update in real time

Generate exportable artifacts for AI IDEs

The application is local-first and does not require authentication.

APPLICATION STRUCTURE

Alchemy consists of:

A React / Next.js frontend

A Python (FastAPI) backend

Local storage for project state and checkpoints

No external database (initial MVP)

No cloud services (initial MVP)

FRONTEND USER EXPERIENCE

6.1 Home Screen

The home screen contains:

Alchemy logo

“Provide your idea” input

Button to start a new project

A list of previous projects displayed as cards (timestamped artifacts)

6.2 Project Screen Layout

Once inside a project, the UI is split into two main columns:

LEFT COLUMN:

Project artifact viewer

Displays current project documentation or files

Bottom section contains a horizontal carousel of artifacts:

Project specification

Canonical JSON

Implementation roadmap

Prompt list

RIGHT COLUMN:

Chat interface

Message history

Chat input

Chat mode selector

A subtle progress indicator is shown to indicate how far along the roadmap the user is. This indicator is non-interactive.

6.3 Chat Modes

There are three distinct chat modes, each with its own message thread and behavior:

Guided / Roadmap Mode

Primary mode

Follows the predefined question roadmap

Collects design decisions

Updates project specification and JSON

May ask AI-generated follow-up questions

Research Mode

Read-only mode

User can ask questions about design, technologies, or tradeoffs

Has access to project context

NEVER updates project state or artifacts

Update / Edit Mode

Allows the user to request changes to previous decisions

Controlled state mutation

Used for iteration and refinement

Does not disrupt the linear roadmap structure

GUIDED ROADMAP SYSTEM

7.1 Static Roadmap Questions

Alchemy contains a predefined, linear set of core questions that apply to all software projects.

These questions cover:

Purpose and goals

Target users

Functional requirements

Non-functional requirements

Constraints

Technology stack

Frontend architecture

Backend architecture

Data handling

APIs and logic

Deployment assumptions (even if local)

Each question includes:

A stable identifier

A description

Three recommended industry-standard options

A smart AI fallback default

A list of fields it updates in the project specification

7.2 Dynamic AI-Generated Questions

Based on the user’s idea and previous answers, the system may generate additional tailored questions.

These questions:

Are additive

Never overwrite explicit user decisions

Follow the same structure as static questions

Always include recommendations and defaults

DECISION HANDLING & STATE MUTATION

Alchemy must decide whether a user message:

Updates the project specification

Is a research question

Is an edit request

This is done via intent classification.

Rules:

Research mode never mutates state

Guided mode mutates state only when a decision is made

Update/Edit mode allows explicit, validated changes

All valid changes update the canonical project JSON and regenerate artifacts.

CANONICAL PROJECT SPECIFICATION

The canonical project specification represents everything about the project, including:

App description

Goals

Features

User flows

Frontend structure (pages, components, layout)

Backend structure (services, endpoints, logic)

Technology stack

Constraints and assumptions

Decisions made and defaults applied

This specification is stored in structured form (JSON) and is the authoritative state.

CHECKPOINTING & VERSIONING

Alchemy automatically creates checkpoints:

After each answered roadmap question

After each explicit update/edit

Each checkpoint:

Is timestamped

Stores a full snapshot of the canonical JSON

Users can:

Revert to any previous checkpoint

Discard future checkpoints when reverting

When reverting:

All derived artifacts are regenerated

Frontend state is synchronized

ARTIFACT GENERATION

Alchemy generates and maintains the following artifacts:

Human-Readable Project Specification

Plain text explanation of the project

Intended for understanding and sharing

Canonical JSON Specification

Machine-readable source of truth

Used as context for AI IDEs

Implementation Roadmap

Phased plan to build the MVP

Each phase has a complete checklist

Prompt Roadmap

Sequential list of AI prompts

One prompt per phase

Designed to be handed to AI IDEs in order

Artifacts are regenerated automatically when the project state changes.

IMPLEMENTATION ROADMAP GENERATION

The implementation roadmap:

Is derived from the canonical project specification

Reflects the chosen stack and architecture

Is detailed enough to build a complete MVP

Is divided into phases with checklists

The roadmap is designed to be translated directly into prompts.

PROMPT ROADMAP COMPILATION

Each roadmap phase is converted into exactly one AI prompt.

Each prompt:

Includes the relevant subset of project context

Has a clear scope

Implements all tasks for that phase

Avoids ambiguity

Assumes sequential execution

The prompt list is exportable.

BACKEND ARCHITECTURE

The backend:

Is implemented in Python using FastAPI

Handles all project state

Performs schema validation

Generates artifacts

Interfaces with the LLM

Enforces chat mode rules

Manages checkpoints

The backend contains no UI logic.

FRONTEND ↔ BACKEND INTEGRATION

All frontend actions:

Are routed through the backend

Receive updated state and artifacts

Trigger UI updates

Frontend:

Displays state

Collects user input

Renders artifacts

Handles navigation and UX

The frontend does not contain business logic.

AI USAGE

Alchemy uses an LLM to:

Generate dynamic questions

Recommend options

Summarize decisions

Generate documentation

Generate roadmaps

Generate prompts

AI decisions are constrained by:

Explicit schema

Existing user choices

Deterministic rules

NON-GOALS (MVP)

Alchemy does NOT:

Build production-ready software

Deploy applications

Replace developers

Automatically execute prompts

Require accounts or authentication

Use cloud storage

SUCCESS CRITERIA

Alchemy is successful if:

A user can start with a vague idea

Follow the guided roadmap

End with a complete project specification

Export prompts and JSON

Use them to bootstrap an MVP in an AI IDE