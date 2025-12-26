# Quickstart Guide: Frontend UI Development

## Prerequisites
- Node.js (v16 or higher)
- npm or yarn package manager
- Git
- Code editor (VS Code recommended)

## Setup Instructions

### 1. Clone and Install Dependencies
```bash
git clone <repository-url>
cd <project-directory>
npm install
```

### 2. Project Structure Overview
```
frontend/
├── src/
│   ├── css/
│   │   └── custom/
│   │       └── custom.css      # Theme styles
│   ├── pages/
│   │   └── index.tsx           # Homepage
│   ├── components/
│   │   ├── HeroSection.tsx     # Hero component
│   │   └── CardsSection.tsx    # Cards component
│   └── styles/
│       └── animations.css      # Animation styles
├── static/
│   └── img/                    # Image assets
└── docusaurus.config.js        # Docusaurus configuration
```

### 3. Start Development Server
```bash
npm run start
```
This will start the Docusaurus development server at http://localhost:3000

### 4. Key Configuration Files
- `src/css/custom/custom.css` - Custom themes and global styles
- `src/pages/index.tsx` - Homepage layout and components
- `docusaurus.config.js` - Site configuration and theme settings

### 5. Theme Development
To modify themes:
1. Edit CSS variables in `src/css/custom/custom.css`
2. Use `.light-theme` and `.dark-theme` classes
3. Test theme switching functionality

### 6. Component Development
To create/edit components:
1. Create components in `src/components/`
2. Import and use in `src/pages/index.tsx`
3. Follow TypeScript interfaces for props

### 7. Build for Production
```bash
npm run build
```
This generates optimized static files in the `build/` directory.

## Common Tasks

### Add New Module Card
1. Add image to `static/img/`
2. Update CardsSection component with new card data
3. Ensure responsive design for all screen sizes

### Update Theme Colors
1. Modify CSS variables in `src/css/custom/custom.css`
2. Test both light and dark themes
3. Verify accessibility contrast ratios

### Add Animations
1. Define animation in `src/styles/animations.css`
2. Apply to elements using CSS classes
3. Test performance across different devices