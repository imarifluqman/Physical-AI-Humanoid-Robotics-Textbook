---
id: 1
title: "Frontend UI Spec – Physical AI & Humanoid Robotics Book"
stage: "spec"
date: "2025-12-24"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "frontend-ui"
branch: "001-frontend-ui"
user: "Marhaba"
command: "/sp.specify"
labels: ["frontend", "ui", "theme", "docusaurus"]
links:
  spec: "specs/001-frontend-ui/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-frontend-ui/spec.md"
  - "specs/001-frontend-ui/checklists/requirements.md"
tests: []
---

## PROMPT_TEXT

```
📘 Frontend UI Spec – Physical AI & Humanoid Robotics Book

Scope: This document defines the frontend UI specifications for the “Physical AI & Humanoid Robotics” book website built with Docusaurus. It covers themes, fonts, page structure, components, animations, images, and colors.

1. Objective

Replace Docusaurus default UI with a custom professional UI.

Implement Light & Dark themes with specific colors.

Add minor animations for hover effects on navbar items, cards, and buttons.

Design Homepage and Cards sections with book module content and images.

Ensure Docs pages and Chatbot follow custom theme colors.

2. Fonts

Font: Josefin Sans

Import URL:

@import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:ital,wght@0,100..700;1,100..700&display=swap');


Usage: Apply across headings, paragraphs, buttons, cards, and all UI elements.

3. Theme Specification
3.1 Light Theme
Element    Color
Background    #eddef1
Main headings, cards background, button background    #412478
Paragraph / other text    White / Black (r Dark Theme
Element    Color
Background    #000000
Main headings, cards background, button background    #eb4a4a
Paragraph / other text    White
3.3 Notes

Themes managed in src/css/custom/custom.css using CSS variables.

Hover animations:

Navbar items: slight scale or underline animation.

Cards: or shadow effect.

4. Folder & File Structure
frontend/
├─ src/
│  ├─ css/
│  │  └─ custom/
│  │      └─ custom.css      <-- Light & Dark themes combined
│  ├─ pages/
│  │  └─ index.tsx           <-- Main homepage
│  ├─ components/
│  │  ├─ HeroSection.tsx     <-- Hero section component
│  │  ├─ CardsSection.tsx    <-- Cards section component
│  │  └─ Chatbot/            <-- Chatbot component
├─ static/
│  └─ img/
│      ├─ robot.jpg          <-- Hero image
│      ├─ module1.jpg        <-- Module 1 image
│      ├─ module2.jpg        <-- Module 2 image
│      ├─ module3.jpg        <-- Module 3 image
│      └─ module4.jpg        <-- Module 4 image

5. Homepage (index.tsx)
5.1 Layout

Left Side:

Book name: Physical AI & Humanoid Robotics (heading).

Paragraph: short intro about the book content.

Button: Get Started → redirects to /docs/intro.

Right Side:

Image: /img/robot.jpg

5.2 Componentization

HeroSection.tsx props:

<HeroSection
  title="Physical AI & Humanoid Robotics"
  description="Explore the cutting-edge intersection of AI and humanoid robotics through practical modules and hands-on experiments."
  buttonText="Get Started"
  buttonLink="/docs/intro"
  image="/img/robot.jpg"
/>

6. Cards Section
6.1 Cards Content

CardsSection.tsx will display 4 cards, each with a module image:

Module    Title    Description    Image
1    The Robotic Nervous System (ROS 2)    Middleware for robot control, ROS 2 Nodes, Topics, Services, bridging Python Agents, URDF for humanoids.    /img/module1.jpg
2    The Digital Twin (Gazebo & Unity)    Physics simulation, environment building, high-fidelity rendering, human-robot interaction, simulating sensors (LiDAR, Depth Cameras, IM --text-color-light: #000000;
  --text-color-light-secondary: #ffffff;

  /* Dark Theme Variables */
  --bg-color-dark: #000000;
  --main-color-dark: #eb4a4a;
  --text-color-dark: #ffffff;
  --text-color-dark-secondary: #cccccc;
}

/* ===========================
   Theme Classes
=========================== */
.light-theme {
  background-color: var(--bg-color-light);
  color: var(--text-color-light);
  font-family: 'Josefin Sans', sans-serif;
}

.light-theme h1, .light-theme h2, .light-theme h3,
.light-theme .card, .light-theme .btn {
  color: var(--main-color-light);
}

.dark-theme {
  backgrThe AI-Robot Brain (NVIDIA Isaac™)    Advanced perception, photorealistic simulation, synthetic data generation, hardware-accelerated VSLAM, Nav2 path planning.    /img/module3.jpg
4    Vision-Language-Action (VLA)    Convergence of LLMs & robotics, voice-to-action with OpenAI Whisper, cognitive planning, capstone project with autonomous humanoid.    /img/module4.jpg
6.2 Card Design

Hover animation: subtle lift or shadow.

Heading: main theme color (#412478 light / #eb4a4a dark).

Background: main heading color with readable text.

Paragraph: contrasting text color.

Image: placed at top of the card.

7. Docs Pages

Maintain default Docusaurus docs structure.

Apply custom theme colors only (background, headings, text).

No layout or content changes.

8. Chatbot Component

Location: src/components/Chatbot

Keep functionality intact.

Apply theme colors only: background, headings, text, and buttons.

No other structural changes.

9. Animations
Element    Animation
Navbar items    Slight scale-up or underline on hover (duration ound-color: var(--bg-color-dark);
  color: var(--text-color-dark);
  font-family: 'Josefin Sans', sans-serif;
}

.dark-theme h1, .dark-theme h2, .dark-theme h3,
.dark-theme .card, .dark-theme .btn {
  color: var(--main-color-dark);
}

/* ===========================
   Animations
=========================== */
.navbar-item:hover {
  transform: scale(1.05);
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0,0,0,0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn:hover {
  opacity: 0.85;
  transition: opacity 0.15s ease;
}

11. Implementation Notes

Apply .light-theme or .dark-theme class to <body> or main container.

HeroSection and CardsSection imported and rendered in index.tsx.

Ensure responsive design for mobile and tablet.

Use CSS variables for easy theme switching.

Docs pages and Chatbot remain functional, inheriting theme colors.

Card images: Each card should have its module-specific image at the top.

12. References

Docusaurus Folder Structure

Josefin Sans Google FontUs).    /img/module2.jpg
3    subtle lift eadable)
3.2
```

## RESPONSE_TEXT

Created comprehensive frontend UI specification for the Physical AI & Humanoid Robotics book website. The specification includes:

- 5 user stories covering homepage UI, theme switching, module cards, documentation theming, and chatbot integration
- 13 functional requirements covering font implementation, theme specifications, animations, component layouts, and responsive design
- 7 success criteria with measurable outcomes for performance, consistency, and user experience
- Quality checklist confirming all requirements are met

The specification is ready for the planning phase and follows all required format and quality standards.