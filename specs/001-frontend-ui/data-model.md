# Data Model: Frontend UI Components

## Theme Entity
- **name**: Theme configuration
- **fields**:
  - themeType: string (light | dark)
  - backgroundColor: string (hex color code)
  - primaryColor: string (hex color code for headings/cards/buttons)
  - textColor: string (hex color code)
  - textSecondaryColor: string (hex color code)
- **relationships**: Applied to UI components globally
- **validation**: Color codes must be valid hex values

## Homepage Component Entity
- **name**: Main landing page structure
- **fields**:
  - heroTitle: string (book title)
  - heroDescription: string (book description)
  - heroButtonText: string (button text)
  - heroButtonLink: string (button destination URL)
  - heroImage: string (image path)
  - cards: array of ModuleCard entities
- **relationships**: Contains HeroSection and CardsSection components
- **validation**: All fields required, image path must exist, button link must be valid URL

## ModuleCard Entity
- **name**: Book module representation
- **fields**:
  - moduleId: string (unique identifier)
  - title: string (module title)
  - description: string (module description)
  - imageUrl: string (path to module image)
  - link: string (destination URL for module)
- **relationships**: Part of CardsSection component
- **validation**: All fields required, image path must exist, link must be valid URL

## Animation Entity
- **name**: UI animation configuration
- **fields**:
  - element: string (navbar | card | button)
  - hoverEffect: string (scale | translateY | opacity)
  - transitionDuration: number (in milliseconds)
  - animationProperties: object (specific animation values)
- **relationships**: Applied to UI elements during hover events
- **validation**: Duration must be positive number, element must be valid type

## Font Entity
- **name**: Typography configuration
- **fields**:
  - fontFamily: string (Josefin Sans)
  - importUrl: string (Google Fonts URL)
  - fontSize: object (size specifications for different elements)
  - fontWeight: string | number (font weight specifications)
- **relationships**: Applied to all text elements globally
- **validation**: Font family and import URL required