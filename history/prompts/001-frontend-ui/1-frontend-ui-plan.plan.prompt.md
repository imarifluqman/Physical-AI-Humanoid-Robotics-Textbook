---
id: 1
title: "Frontend UI Plan"
stage: "plan"
date: "2025-12-24"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "frontend-ui"
branch: "001-frontend-ui"
user: "Marhaba"
command: "/sp.plan"
labels: ["frontend", "ui", "theme", "docusaurus", "implementation"]
links:
  spec: "../../specs/001-frontend-ui/spec.md"
  plan: "../../specs/001-frontend-ui/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-frontend-ui/plan.md"
  - "specs/001-frontend-ui/research.md"
  - "specs/001-frontend-ui/data-model.md"
  - "specs/001-frontend-ui/quickstart.md"
  - "specs/001-frontend-ui/contracts/theme-api.yaml"
tests: []
---

## PROMPT_TEXT

```
🧭 Frontend UI Implementation Plan

Project: Physical AI & Humanoid Robotics (Docusaurus)

1. Planning Overview

Goal:
Docusaurus ke default UI ko replace karke ek custom professional frontend UI banana jisme:

Custom Light & Dark themes

Consistent Josefin Sans font

Professional Homepage (Hero + Cards)

Docs pages par sirf colors apply hon

Chatbot ka UI theme ke sath match kare

Subtle animations for better UX

2. Initial Cleanup & Preparation
2.1 Default UI Cleanup

Landing page se:

Default Docusaurus hero

Default cards

Default text sections
remove kiye ja chuke hain ✅

2.2 Folder Verification

Ensure ye folders exist karte hon:

src/css/custom/custom.css
src/pages/index.tsx
src/components/
static/img/

3. Theme Implementation Plan
3.1 Theme Strategy

Single CSS file: src/css/custom/custom.css

CSS Variables use hongi

.light-theme aur .dark-theme classes se theme switch hoga

Default Docusaurus theme colors override honge

3.2 Light Theme Colors

Background: #eddef1

Primary / Headings / Cards / Buttons: #412478

Text: Black / White (readability ke mutabiq)

3.3 Dark Theme Colors

Background: #000000

Primary / Headings / Cards / Buttons: #eb4a4a

Text: White

3.4 Font Setup

Google Font: Josefin Sans

Font import custom.css ke top par

Apply globally (body, headings, buttons, cards, chatbot)

4. Animations Plan
4.1 Navbar

Hover par:

Slight scale OR

Underline animation

Duration: 150–200ms

4.2 Cards

Hover par:

Slight lift (translateY)

Soft shadow

Duration: 200ms

4.3 Buttons

Hover par:

Smooth background / opacity transition

Duration: 150ms

5. Homepage Structure Plan

File: src/pages/index.tsx

Homepage 2 major sections contain karega:

5.1 Hero Section (Component Based)

Component: HeroSection.tsx

Layout

Left Side:

Book Title
"Physical AI & Humanoid Robotics"

Short professional paragraph (book intro)

Get Started button
→ /docs/intro

Right Side:

Image:
/static/img/robot.jpg

Design Rules

Clean spacing

Responsive layout

Button theme color follow kare

Professional look (no clutter)

6. Cards Section Plan

Component: CardsSection.tsx

6.1 Total Cards

4 Cards

Each card = 1 Module

6.2 Card Structure (Same for all)

Each card must contain:

Top Image (module specific)

Module Title

Short Description

Clean spacing & hover animation

6.3 Card Images

Images location:

static/img/module1.jpg
static/img/module2.jpg
static/img/module3.jpg
static/img/module4.jpg

6.4 Card Content Mapping
Module 1

Title: The Robotic Nervous System (ROS 2)

Focus: Middleware, ROS 2, Nodes, Topics, URDF

Module 2

Title: The Digital Twin (Gazebo & Unity)

Focus: Physics simulation, sensors, environments

Module 3

Title: The AI-Robot Brain (NVIDIA Isaac™)

Focus: Perception, SLAM, navigation, training

Module 4

Title: Vision-Language-Action (VLA)

Focus: LLMs + Robotics, voice commands, capstone project

7. Docs Pages Plan
Scope

NO layout change

NO content change

Actions

Default Docusaurus docs UI rahegi

Sirf:

Background color

Text color

Heading color
custom theme ke mutabiq apply honge

8. Chatbot UI Plan

Location: src/components/Chatbot

Rules

Functionality bilkul same rahe

Sirf colors theme ke mutabiq change

Background

Text

Buttons

Headings

No Changes

Logic

APIs

Behavior

9. Responsiveness Plan

Mobile

Tablet

Desktop

Ensure:

Hero section stack ho jaye small screens par

Cards grid responsiv
```

## RESPONSE_TEXT

Successfully created the implementation plan for the frontend UI of the Physical AI & Humanoid Robotics book website. The plan includes:

1. Complete implementation plan document (plan.md) outlining the technical approach
2. Research document (research.md) resolving technical unknowns and documenting decisions
3. Data model (data-model.md) defining the entities for the UI components
4. Quickstart guide (quickstart.md) for developers to set up and work with the frontend
5. API contract (contracts/theme-api.yaml) for theme switching functionality

The plan follows the constitution principles and addresses all requirements from the feature specification. The implementation will use Docusaurus with custom CSS themes, React components for the homepage sections, and proper responsive design.