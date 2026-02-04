Alchemy: Problems To Solve

# chat modes 
1. There are 3 Chat Modes - each chat should have context on the project, but they should all have distinct views with their own message threads (no crossover)
- Guided/roadmap: The rough pre-defined question set at the core (questions that are true reguardless of app type) and then tailored questions based on their specific idea. The user should answer using preset or custom answers, but the llm should also ask smart follow-ups
- Research: The user is able to ask questions related to app design. This chat mode has access to the project context, but will not make any updateds to the project spec.
- Update/edit: Again, it should have context about the projects current state. the user is allowed to specifically request changes in this chat mode and go back and forth without overloading their roadmap/timeline chat.


# edit or question decision 
2: for messages in the guided/roadmap chat and the update/edit chat, the llm or ai should be able to dynamically assess each message and decide wether to update the project specification files or not - it should not update for general queries or question, but only if the user makes changes or design decisions.


# formula
3: refine and iterate on the question set - this is the formula/secret sauce. the whole purpose of this app is to allow people to design and create software even if they don't know all the criteria, questions to ask, or technical requirements that they need to define. this app should have a rough roadmap that they are able to follow, and the user can answers these core questions to get a well-rounded foundation, and then the ai/llm should also dynamically ask other question ontop of this core question set based on the users specific idea. for each question int he roadmap chat, the ai will provide 3 recommended options if the doesn't know what to choose. we must define the core questions - purpose, functionality, technologies, libraries, tools, frontend & backend architecture, Backend structure (smart suggestions based on required functionality and features), frontend UI/UX pages and components (smart recommendations based on app archetype, purpose, and functionality), etc (everything). after everything is well defined, and some project specific questions have been ask ontop of these core questions, the ai should be able to create a roadmap or implementation plan of phases/steps and each phase should provide a complete checklist of tasks to complete for that phase. This roadmap is then converted into a prompt list and all the user has to do is to hand the prompts 1 by 1 to the ai/llm and let it do the rest. this gives them an mvp of the app and then they can continue to refine and iterate on the app.

# how to maintain context
4: 



How Is This Going To Maintain Context? how do i efficiently handle tokens when im going to have a whole chat history of questions for the 3 chat modes? 

How Am I Going To Save The Project Checkpoints, are they stored locally, github, whats the solution?

Home Screen: 
- Previous Artifact Project Cards At The Bottom so the user can access previous sessions
- Update Button lables/text
- new Logo

Project Screen:
- Add Buttons For Settings (custom options such as api tokens and project settings) & Donwload/Export
- Change Project Files Too Cards
- Add Revert/restore Checkpoint buttons at each previous message from the user like cursor and anti-gravity





















# Guided Roadmap Questions
What problem are you trying to solve?

Who is this product for?

What pain point does this solve for the user?

What defines success for the MVP?

Are there any hard constraints (time, budget, solo dev, demo-only)?

What type of software is this (web app, backend service, CLI, other)?

What is the primary app archetype (dashboard, workflow tool, document-based, etc)?

Is the application stateful or stateless?

What are the core user actions the app must support?

Does the app require user accounts or authentication?

Does the app require real-time or near-real-time behaviour?

What data entities does the app manage?

Is data persistence required?

Where should data be stored (local, database, external APIs)?

What is the expected data scale for v1?

What is the primary user interface style?

How complex should the UI be?

Is the app desktop-first, responsive, or mobile-first?

Which frontend framework should be used?

What styling approach should be used?

How should frontend state be managed?

Does the app require a backend?

What responsibilities does the backend have?

What API style should the backend expose?

What backend language/runtime should be used?

What backend framework should be used?

What database should be used?

Does the app use AI or LLMs?

What role does AI play in the app?

Are there performance constraints?

Are there security or privacy concerns?

Is this application intended for internal use or public use?

What level of polish is required for the MVP?



PHASE L — FRONTEND PAGE STRUCTURE

What pages or views does the application require?

Which page is the primary entry point?

Are there modal-based flows or full-page navigation?

Does the app require a persistent layout (sidebar/header)?

Should navigation be hidden, minimal, or explicit?

Does the app require multi-step or wizard-style flows?

PHASE M — FRONTEND COMPONENT DESIGN

What reusable UI components are required?

Are there domain-specific components (editors, tables, cards, timelines)?

Does the app require a chat-style interface?

Are there read-only vs editable views?

Does the app require drag-and-drop or advanced interactions?

What UI state must persist across pages?

PHASE N — FRONTEND LAYOUT & UX LOGIC

How is screen space divided (single column, split view, dashboard grid)?

Are there primary and secondary panels?

Does the app require real-time UI updates?

How are loading, empty, and error states handled?

How should undo/revert actions behave?

How should the app indicate progress or completion?

PHASE O — FRONTEND FILE & FOLDER STRUCTURE

How should frontend files be organised?

Should pages and components be colocated?

Should there be a shared UI/components layer?

Should state management live globally or per feature?

How should styles be structured?

PHASE P — BACKEND RESPONSIBILITY BREAKDOWN

What business logic must live in the backend?

Which operations are read-only vs mutating?

Does the backend orchestrate AI calls?

Does the backend manage workflows or state machines?

Are background tasks or async jobs required?

PHASE Q — BACKEND API DESIGN

What API endpoints are required?

What does each endpoint do?

What data does each endpoint accept and return?

Are endpoints public or internal-only?

How should errors be handled and returned?

Is versioning required for the API?

PHASE R — BACKEND DATA & MODELS

What are the core backend data models?

What relationships exist between models?

Which fields are required vs optional?

Are there computed or derived fields?

How should migrations be handled?

PHASE S — BACKEND FILE & FOLDER STRUCTURE

How should backend code be organised?

Should routes, services, and models be separated?

Where does AI logic live?

Where does validation live?

Where does configuration live?

PHASE T — AI INTEGRATION STRUCTURE (IF APPLICABLE)

Which backend components call the LLM?

How is prompt context assembled?

How is structured output enforced?

How are AI defaults vs user decisions distinguished?

How are AI failures handled?

PHASE U — DERIVED ARTIFACT GENERATION

How is the human-readable specification generated?

How is the canonical JSON spec generated?

How is the implementation roadmap generated?

How are sequential AI prompts generated?

What assumptions are embedded into prompts?

PHASE V — PROMPT EXECUTION STRATEGY

Are prompts frontend-first or backend-first?

Should prompts be framework-specific?

Should prompts be incremental or file-based?

How should the user validate each step?

What is considered a “complete MVP”?

PHASE W — ITERATION & OVERRIDES

How does the user revise earlier decisions?

How are conflicting decisions resolved?

How does the system recompile artifacts after changes?

What happens to downstream prompts after overrides?

PHASE X — CHECKPOINTS & VERSIONING

When are checkpoints created?

What metadata is stored with each checkpoint?

How does revert/restore work?

How are checkpoints displayed to the user?

PHASE Y — EXPORT & HANDOFF

What formats can be exported?

Should exports be partial or complete?

Are exports human-readable, machine-readable, or both?

How does the user hand outputs to an external AI IDE?

PHASE Z — MVP COMPLETION CRITERIA

What does “MVP complete” mean for this project?

What remains intentionally out of scope?

What are logical next iteration steps?


















# ChatGPT Response
✔ Correct intended flow

User answers guided roadmap questions

Answers mutate canonical JSON

Alchemy generates:

Human-readable documentation

Implementation roadmap (phases + checklists)

That roadmap is translated into:

A prompt roadmap

User exports:

JSON spec

Documentation

Prompt list

User feeds prompts + JSON to Cursor / AI IDE

MVP is bootstrapped

This is exactly the correct mental model.