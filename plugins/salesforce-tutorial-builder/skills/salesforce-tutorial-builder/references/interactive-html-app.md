# Interactive Single-File HTML Tutorial App

Use this workflow for single shareable interactive HTML, local dev server, or both.

## Stack & Directory Architecture

- **Core stack:** Vite + React (JavaScript unless TypeScript is requested), plain CSS with custom properties (no Tailwind, no external UI component library), and `vite-plugin-singlefile` to inline JS/CSS into one portable HTML file.
- **No-Node fallback:** If Node/npm is unavailable in the host environment, emit a clean self-contained HTML file with inline CSS and vanilla ES JavaScript implementing the same 6 interactive controls and design tokens.

```text
tutorial-app/
├── src/
│   ├── main.jsx, App.jsx, index.css
│   ├── context/TutorialContext.jsx      # done map, live config values, active path
│   ├── components/
│   │   ├── Nav.jsx                      # sticky left nav + progress bar + IntersectionObserver
│   │   ├── StepCard.jsx                 # collapsed by default, toggleable, done checkbox
│   │   ├── CopyBlock.jsx                # terminal chrome + copy-to-clipboard button
│   │   ├── Callout.jsx                  # info / warning / tip / error variants
│   │   ├── Tabs.jsx                     # branching deployment/channel paths
│   │   └── ConfigPanel.jsx              # live inputs -> real-time snippet interpolation
│   └── sections/                        # Prerequisites -> Setup -> Embed -> Troubleshoot
├── index.html, vite.config.js, package.json
```

## Vite Single-File Configuration

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  server: { port: 3000 },
  build: {
    target: 'esnext',
    assetsInlineLimit: 100000000,
    chunkSizeWarningLimit: 100000000,
    cssCodeSplit: false,
  }
})
```

## SLDS Design Tokens & Branding

Define all theming via `:root` CSS custom properties in `src/index.css`:
- Brand & accents: `--sf-blue: #0176D3`, `--sf-blue-dark: #014486`, `--sf-blue-light: #D8EDFF`, `--sf-green: #2E844A`, `--sf-green-light: #EAF5EA`, `--sf-orange: #E07816`, `--sf-orange-light: #FEF1E2`, `--sf-red: #C23934`, `--sf-red-light: #FDECEA`, `--sf-purple: #7526E3`, `--sf-purple-light: #F3EEFF`.
- Neutrals: `--sf-gray-1: #F3F3F3`, `--sf-gray-2: #E5E5E5`, `--sf-gray-3: #AEAEAE`, `--sf-gray-4: #706E6B`, `--sf-gray-5: #3E3E3C`, `--sf-text: #181818`, `--sf-white: #FFFFFF`.
- **Branding rules:** Salesforce brand uses hero gradient `linear-gradient(135deg, #014486 0%, #0176D3 60%, #1589ee 100%)`. Custom brand overrides CSS variables and uses only a user-verified public logo URL—otherwise render a crisp text/monogram badge. Neutral uses the baseline tokens without brand logos.

## 6 Mandatory Interactive Controls

1. **Progress tracking:** `TutorialContext` tracks completed steps; sidebar shows `X/Y steps` and visual progress bar.
2. **Collapsible `StepCard`:** Collapsed by default, expands on click, persists done toggle.
3. **Copy-to-clipboard `CopyBlock`:** Wraps every CLI command, XML, JSON, or embed snippet with copied confirmation state.
4. **Live `ConfigPanel`:** Editable fields for org ID, My Domain URL, API names, or deployment IDs initialized with synthetic placeholders (`00D000000000000`, `https://example.my.salesforce.com`); updates all generated snippets live.
5. **Path switching (`Tabs`):** When multiple deployment paths exist (e.g., Experience Cloud vs. external site), place a path selector in header/context and tabbed instructions per path.
6. **Troubleshooting FAQ:** Collapsible accordion of common errors and fixes as the final section.

## Build, Export & Sharing Handoff

Run `npm install && npm run build`, then copy `dist/index.html` to `../[feature-name]-setup-guide.html`. Verify the build succeeds and the output file is non-empty. Share instructions with the user: open directly in any browser, attach via email/Slack, upload to Google Drive/Confluence/SharePoint, or host on any static CDN; use `npm run dev` inside `tutorial-app` for live editing and `npm run build` to re-export.
