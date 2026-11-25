# SLDS 2 Styling Hooks, Accessibility, and Performance

## SLDS 2 & Dark-Mode Compliance

- **Platform base components first**: Prefer `lightning-button`, `lightning-input`, `lightning-datatable`, `lightning-record-picker`, and `lightning-modal` over custom reimplementations.
- **Zero hardcoded colors or spacing**: Use SLDS 2 global styling hooks so components adapt cleanly across SLDS 2 themes and dark mode:

| Styling Need | SLDS 2 Styling Hook Example | Avoid |
| --- | --- | --- |
| Surface background | `var(--slds-g-color-surface-container-1)` | `#ffffff`, `white` |
| Primary text | `var(--slds-g-color-on-surface-2)` | `#181818`, `#333` |
| Brand accent | `var(--slds-g-color-accent-2)` | `#0176d3` |
| Spacing & radius | `var(--slds-g-spacing-4)`, `var(--slds-g-radius-border-2)` | `16px`, `4px` literals |

- **Shadow DOM boundaries**: Never rely on undocumented internal DOM structure of base Lightning components. Customize base components only through documented `--slds-c-*` component styling hooks or variants.
- **No inline style abuse**: Keep styling in `<component>.css` using SLDS 2 utility classes and CSS custom properties; reserve inline styles for truly dynamic numeric measurements.

## Accessibility (WCAG 2.1 AA)

- **Semantic HTML first**: Use native `<button>`, `<label>`, headings (`<h1>`–`<h3>` in logical order), and landmark roles instead of clickable `<div>` or `<span>` elements.
- **ARIA & live regions**: Provide `aria-label` or `alternative-text` on icon-only buttons; use `role="status"` / `aria-live="polite"` for async loading or filter counts and `role="alert"` for error banners.
- **Keyboard & focus management**: Every interactive control must be reachable via `Tab` and activatable via `Enter`/`Space`. Modals must trap focus, restore focus to the triggering element on close, and close on `Escape` (prefer `LightningModal` from `lightning/modal`).
- **Form validation & contrast**: Associate error messages via `aria-describedby` or base component `setCustomValidity()`/`reportValidity()`. Maintain at least 4.5:1 text contrast (3:1 for large text/UI components) using SLDS 2 semantic tokens.
- **Never suppress focus outlines**: Do not write `outline: none` without a visible high-contrast `:focus-visible` replacement.

## Performance & Rerender Safety

- **Protect `renderedCallback()`**: Never mutate reactive tracked state unconditionally inside `renderedCallback()` — it causes infinite rerender loops. Gate one-time DOM initialization behind a private boolean flag (`this._initialized`).
- **Keep getters lightweight**: Template getters run on every render cycle. Never run expensive sorting, filtering, or API calls inside getters; precompute on data arrival or memoize.
- **Debounce user input**: Debounce search inputs (`300 ms`) before invoking imperative Apex or GraphQL refetches; clear pending `setTimeout` timers in `disconnectedCallback()`.
- **Lazy rendering & lists**: Always supply a stable unique `key` on `for:each` / `iterator:*` items (never array index for mutable lists). Render heavy tab/modal content conditionally with `lwc:if` / `lwc:elseif` / `lwc:else` (prefer over legacy `if:true` / `if:false`).
- **Memory hygiene**: Remove `window` event listeners, `IntersectionObserver` instances, and LMS subscriptions inside `disconnectedCallback()`.

## Template Anti-Patterns to Catch Early

| Anti-Pattern | Risk | Safe Alternative |
| --- | --- | --- |
| Inline calls or operators on older orgs (`{items.length}`, `{a + b}`) | Compile error or lint violation before complex expressions GA | Compute in a lightweight JS getter |
| Inline args in event handlers (`onclick={handleClick(item.id)}`) | Invalid LWC template syntax | Pass `data-id={item.id}` and read `event.currentTarget.dataset.id` |
| Legacy `if:true` / `if:false` | Deprecated directive | Use `lwc:if`, `lwc:elseif`, `lwc:else` |
| Array index as `for:each` `key` | Broken DOM reconciliation on reorder/delete | Use stable record `Id` or unique key |

## Bundle Quality Checklist

- Explicit loading (`lightning-spinner` with `alternative-text`), empty, and sanitized error states rendered cleanly in the template
- All interactive controls tested with keyboard-only navigation and validated with `scripts/validate_slds.py`
- `.js-meta.xml` declares exact `<apiVersion>`, `<isExposed>`, `<targets>`, and `<targetConfigs>` with descriptive `masterLabel` and `description`
