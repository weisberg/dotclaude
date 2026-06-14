---
name: expo-mobile-app
description: Build, review, refactor, and modernize Expo and React Native apps for iOS, Android, and web. Use for Expo Router, app architecture, beautiful mobile UI, design systems, animations, accessibility, performance, native modules, testing, EAS Build/Update, and improving existing Expo code.
---

# Expo Mobile App Skill

## Mission

Create and improve Expo applications that feel native, look distinctive, run smoothly, and remain maintainable across iOS, Android, and web. Favor Expo-first, TypeScript-first, accessible, performance-aware solutions that fit the existing codebase instead of imposing a rewrite.

## Activation triggers

Use this skill when the task mentions Expo, React Native, mobile apps, iOS, Android, web, Expo Router, EAS, OTA updates, app navigation, app UI, screens, components, design systems, animations, gestures, haptics, accessibility, app performance, native modules, app icons, splash screens, or refactoring an Expo codebase.

## Core principles

1. **Inspect before editing.** Read the project structure, `package.json`, app config, routing layout, UI primitives, and styling approach before making changes.
2. **Prefer Expo conventions.** Use Expo Router for new Expo apps, Expo SDK packages when available, `npx expo install` for Expo-aware dependency versions, config plugins for native configuration, and development builds when native behavior must change.
3. **Design is part of the code.** Treat every screen as a product surface with hierarchy, state design, accessibility, motion, responsive behavior, and platform fit.
4. **Preserve what works.** In existing apps, match the established architecture, package manager, styling library, component naming, lint rules, and design language unless they are causing the problem.
5. **Ship in small verified steps.** Make focused changes, run the relevant checks, fix regressions, and summarize exactly what changed.

## First-pass project audit

Before changing an existing app, inspect the files that define behavior and conventions:

- `package.json`, lockfile, scripts, Expo SDK version, React Native version, package manager.
- `app.config.*`, `app.json`, `eas.json`, `babel.config.*`, `metro.config.*`, `tsconfig.json`, lint/test config.
- `app/` or `src/app/` route tree, especially `_layout.tsx`, route groups, modals, tabs, auth flows, and deep-link assumptions.
- Shared UI primitives, design tokens, theme provider, icon system, typography, color mode handling.
- Data layer: API client, auth/session storage, query/cache layer, local database/storage, environment variables.
- Platform-specific files and custom native code, if `ios/` or `android/` are committed.
- Existing tests, CI, error tracking, analytics, and release scripts.

When safe and relevant, use the project's own scripts first, then Expo tooling:

```bash
npx expo-doctor
npx expo lint
npx tsc --noEmit
npm test
```

Adapt commands to the detected package manager and scripts. Do not run destructive commands, dependency upgrades, prebuild cleanups, or long builds unless they are necessary for the task.

## Working on existing code

1. Identify the smallest change that improves the app without destabilizing unrelated flows.
2. Keep imports, file placement, component style, and naming consistent with the repository.
3. Avoid replacing the navigation, styling, state, or data stack just because a different stack is fashionable.
4. Prefer extracting reusable UI primitives over copying styles across screens.
5. When refactoring, preserve behavior first, then improve structure, then improve visual polish.
6. Check for user changes with `git status` before large edits. Do not overwrite unrelated work.
7. After edits, run the narrowest useful validation. If a check fails because of pre-existing issues, report that separately from new issues.

## Foundation for new Expo apps

Default to this foundation unless the user or repo clearly indicates otherwise:

- Expo Router with the `app/` directory and TypeScript.
- Feature-oriented code organization with shared UI primitives.
- A small design-token layer before adding a large UI framework.
- `react-native-safe-area-context` at the root and screen-level safe-area handling.
- `expo-font` and a controlled splash-screen flow when custom fonts or assets must load before first paint.
- `userInterfaceStyle: "automatic"` when dark mode is supported.
- EAS profiles for development, preview, and production when distribution matters.
- Jest/RNTL tests for reusable components and business logic.

Recommended structure for new or reorganized apps:

```text
app/
  _layout.tsx
  index.tsx
  (auth)/
  (tabs)/
  modal.tsx
components/
  ui/
  screen/
features/
  home/
  profile/
  settings/
design/
  tokens.ts
  theme.ts
  typography.ts
lib/
  api/
  auth/
  storage/
  validation/
hooks/
assets/
```

Keep route files thin. Put domain logic in `features/`, shared primitives in `components/ui/`, and platform or infrastructure code in `lib/`.

## Navigation and routing

- Use Expo Router for new Expo projects and for refactors already using the `app/` directory.
- Use route groups like `(tabs)`, `(auth)`, and `(modal)` to express navigation structure without leaking group names into URLs.
- Keep auth routing explicit: protected routes, redirects, and loading states must avoid flashing private screens.
- Use stack, tabs, drawer, and modal patterns only when they match platform expectations and the product flow.
- Every screen should have a stable empty, loading, error, and success state.
- Prefer `Link` for declarative navigation and router methods for event-driven navigation.
- Avoid global navigation side effects from random components; centralize navigation guards in layouts.
- Treat every route as deep-linkable unless there is a strong reason not to.

## Design system rules

First adapt to the app's current styling approach. If there is no coherent approach, build a lightweight token system before adding a third-party UI kit.

Use semantic tokens, not raw values scattered through screens:

```ts
export const spacing = { xs: 4, sm: 8, md: 12, lg: 16, xl: 24, xxl: 32 } as const;
export const radius = { sm: 8, md: 14, lg: 22, full: 999 } as const;
export const color = {
  light: {
    bg: '#FFFFFF',
    surface: '#F7F7F8',
    text: '#111114',
    muted: '#6B6F76',
    accent: '#4F46E5',
    danger: '#D92D20',
  },
  dark: {
    bg: '#090A0D',
    surface: '#15171C',
    text: '#F6F7F9',
    muted: '#A4A8B0',
    accent: '#8B7CFF',
    danger: '#FF6B6B',
  },
} as const;
```

Design tokens should cover:

- Color: background, surface, surface elevation, text, muted text, borders, accent, success, warning, danger.
- Typography: display, title, body, label, caption, line heights, weights, dynamic type behavior.
- Spacing: consistent scale for layout, cards, controls, and section rhythm.
- Shape: radius scale for buttons, cards, sheets, avatars, chips.
- Elevation: iOS shadow and Android elevation equivalents.
- Motion: durations, easing, spring presets, reduced-motion fallbacks.

Create reusable primitives such as `Screen`, `Text`, `Button`, `IconButton`, `Card`, `ListRow`, `TextField`, `Badge`, `Avatar`, `EmptyState`, `ErrorState`, `Skeleton`, and `BottomSheet` before building many one-off components.

## Beautiful and innovative UI standards

Every meaningful UI change should improve at least one of these:

- **Clarity:** The primary action and information hierarchy are obvious in three seconds.
- **Tactility:** Press, drag, selection, refresh, and completion states feel responsive through visual feedback, haptics, or motion.
- **Depth:** Cards, sheets, overlays, and backgrounds create spatial hierarchy without clutter.
- **Continuity:** Transitions preserve context between list/detail, create/edit, and modal flows.
- **Personality:** The product has one or two signature moments rather than generic template screens.
- **Resilience:** Empty, offline, permission-denied, loading, and error states are as designed as the happy path.

When creating a new screen, reason through:

1. User goal and emotional tone.
2. Visual hierarchy and primary action.
3. Platform-specific navigation/header behavior.
4. State matrix: loading, empty, partial data, offline, error, permission denied, success.
5. Accessibility labels, focus order, text scaling, contrast, touch target size.
6. Motion/haptics that reinforce state changes without slowing the user.
7. Responsive behavior for small phones, large phones, tablets, and web.

Avoid novelty for novelty's sake. Innovative UI should make the app easier, calmer, faster, or more memorable.

## Platform fit

Use shared code where it improves consistency, and platform-specific code where it improves quality.

| Concern | Preferred handling |
|---|---|
| Safe areas | Use `react-native-safe-area-context`; avoid hardcoded top/bottom padding. |
| Status bar | Match screen background and modal presentation; test light and dark. |
| Keyboard | Ensure forms remain usable with software keyboard, hardware keyboard, and screen readers. |
| Android back | Define expected behavior for modals, nested stacks, forms, and unsaved changes. |
| Haptics | Use sparingly for success, warning, selection, impact, and important transitions. |
| Gestures | Use native gesture handling for drag/swipe/pan interactions. |
| Web | Add responsive widths, keyboard focus, hover/pressed states, and accessible landmarks where applicable. |
| Tablet | Avoid stretched phone layouts; use max widths, sidebars, two-pane layouts, or richer spacing. |

Use `Platform.select` for real platform differences, not as a dumping ground for inconsistent styles.

## Accessibility requirements

Accessibility is not optional and should be built into primitives.

- Prefer at least 44x44 logical pixels for important touch targets; never go below WCAG minimums without an equivalent accessible control.
- Do not rely on `hitSlop` alone to satisfy accessibility target size; the visible and accessibility focus area should make sense.
- Add `accessibilityRole`, `accessibilityLabel`, `accessibilityHint`, and `accessibilityState` for custom controls.
- Ensure icons without visible text have useful labels; decorative icons should not be announced.
- Support text scaling and avoid fixed-height containers that clip larger text.
- Preserve logical screen-reader order. Avoid absolute positioning that creates confusing focus order.
- Manage focus after opening modals, completing forms, showing errors, or navigating after async work.
- Do not communicate meaning through color alone.
- Respect reduced motion for non-essential animations.
- Test key flows with VoiceOver/TalkBack assumptions in mind, not just visual inspection.

## Animation, gestures, and haptics

- Use Reanimated for high-frequency, gesture-linked, or layout-sensitive animation.
- Keep animations purposeful: feedback, continuity, causality, or delight.
- Use native-thread gestures for drag, swipe, pull-to-refresh, sliders, reorder, and sheets.
- Avoid JS-thread animation loops during scrolling or gesture tracking.
- Use springs for physical interactions and short timing animations for opacity/color/transform feedback.
- Provide reduced-motion alternatives for decorative movement.
- Add haptics only at meaningful moments; never buzz on every minor touch.

Good signature interactions include:

- A list item that smoothly expands into a detail card.
- A bottom sheet that previews the next step and snaps predictably.
- A tactile success state after completing a task.
- A playful empty state that still guides the user to the next action.
- A polished skeleton-to-content transition that avoids layout shift.

## Performance standards

Aim for native-feeling 60 FPS interactions and fast perceived startup.

- Profile before large optimizations. Identify whether the issue is JS work, UI work, layout, images, list virtualization, network, or startup.
- Keep route files and top-level providers lean.
- Split state so one interaction does not re-render the entire app tree.
- Use memoization when it prevents real re-renders, not as decoration.
- Use `FlashList` or well-tuned virtualized lists for large or complex lists.
- Keep list item render functions stable; use stable keys and item types for heterogeneous lists.
- Avoid unbounded `ScrollView` for large data sets.
- Use `expo-image` or the project's image abstraction for remote image caching, placeholders, and transitions when appropriate.
- Preload critical fonts/assets and keep the splash screen visible only as long as necessary.
- Remove noisy logs and expensive debug-only work from production paths.
- Prefer optimistic UI and local cache for perceived speed, with clear rollback states.

## Data, state, and offline behavior

Separate these concerns:

- **Local UI state:** component state or small focused stores.
- **Server state:** query/cache layer such as TanStack Query when the app already uses it or the project needs caching, retries, invalidation, and stale data handling.
- **Persistent app state:** AsyncStorage or SQLite for non-sensitive data, depending on size and query needs.
- **Sensitive small values:** `expo-secure-store` for tokens and keys; handle native errors and do not store large payloads there.
- **Local-first data:** Expo SQLite with a sync/state layer when the app must work offline as a primary experience.

Networked flows should handle slow, offline, failed, stale, and partial-data states. Avoid blank screens during refetches. Prefer stale-while-revalidate behavior when it fits the product.

## Security and privacy

- Never put private keys, service-role tokens, signing credentials, or real secrets in client code.
- Treat `EXPO_PUBLIC_*` values as public because they are embedded into the client bundle.
- Store tokens in secure storage, not plain AsyncStorage.
- Avoid logging PII, tokens, auth headers, or precise location in development or production logs.
- Validate deep-link parameters and remote config before using them.
- Request permissions only when they are needed and explain why in the UI before the system prompt when helpful.
- Keep environment-specific values in `.env.local`, EAS environment variables, or CI secrets as appropriate.

## Native capabilities and CNG

- Prefer Expo SDK modules before adding custom native dependencies.
- When a native library or native configuration is required, move from Expo Go assumptions to a development build using `expo-dev-client`.
- Prefer app config and config plugins over manual edits to generated native files.
- In Continuous Native Generation projects, treat `ios/` and `android/` as generated unless the repo clearly owns custom native code.
- If manual native edits are unavoidable, document why config plugins are insufficient and isolate the change.
- After adding or changing native code/config, plan for a new build, not only an OTA update.
- Check New Architecture compatibility for third-party native libraries before adding them.

## EAS Build, Update, and release hygiene

- Use `eas.json` profiles for `development`, `preview`, and `production`.
- Keep bundle identifiers, app names, icons, environment variables, channels, and signing credentials environment-aware.
- Use EAS Update for compatible JavaScript and asset changes; do not publish updates that require native code not present in the installed binary.
- Maintain a clear `runtimeVersion` strategy. Update it when the native runtime changes.
- Test preview builds on real iOS and Android devices before production release.
- Keep app icon, splash screen, adaptive icon, permissions text, privacy manifests, and store metadata aligned with the actual product.

## Testing and validation

Use the lightest validation that can prove the change:

- Type checks for TypeScript changes.
- Expo lint for code quality and import issues.
- Unit tests for utilities, hooks, reducers, query transforms, validation, and formatting.
- React Native Testing Library for user-observable component behavior and accessibility queries.
- Snapshot tests only when they are stable and meaningful.
- Manual simulator/device checks for navigation, gestures, keyboard behavior, haptics, platform-specific UI, camera/media/notifications, and safe areas.
- Preview EAS builds for native dependency/config changes.

Before finishing a non-trivial task, run or recommend:

```bash
npx expo-doctor
npx expo lint
npx tsc --noEmit
npm test
```

Only include commands that exist or make sense for the project.

## UI implementation checklist

Before marking UI work complete, verify:

- [ ] Screen has clear hierarchy, spacing, and primary action.
- [ ] Loading, empty, error, offline, and success states are represented.
- [ ] Touch targets are large enough and not crowded.
- [ ] Custom controls have accessibility role, label, state, and hint as needed.
- [ ] Layout works on small phones, large phones, tablets, and web if web is supported.
- [ ] Safe areas, keyboard, status bar, and Android back behavior are handled.
- [ ] Dark mode and contrast are acceptable if app supports themes.
- [ ] Animations are smooth, purposeful, and reduced-motion friendly.
- [ ] Lists remain performant with realistic data volume.
- [ ] No secrets, PII logs, or hardcoded environment-specific values were introduced.

## Code quality checklist

Before final response, verify:

- [ ] Changes are minimal and scoped to the request.
- [ ] Existing conventions were preserved or intentionally improved.
- [ ] New components are reusable where repetition was likely.
- [ ] Types are strict enough to catch misuse; avoid `any` unless justified.
- [ ] Dependencies were added only when they meaningfully reduce complexity.
- [ ] Expo packages were installed with Expo-aware commands.
- [ ] Native changes are documented and mapped to build/update implications.
- [ ] Validation commands were run or blockers were clearly explained.

## Common anti-patterns to avoid

- Rewriting the app architecture for a small UI or bug-fix request.
- Adding Redux, a large UI kit, or a styling framework without project need.
- Hardcoding device dimensions, status bar heights, safe-area padding, or platform constants.
- Using absolute positioning for normal layout.
- Building custom buttons without pressed, disabled, loading, accessibility, and focus states.
- Leaving screens with only happy-path UI.
- Using `ScrollView` for large lists.
- Adding native libraries while assuming Expo Go will still be enough.
- Editing generated native projects when a config plugin would solve the problem.
- Publishing OTA updates for changes that require native code changes.
- Storing secrets in `EXPO_PUBLIC_*`, source files, or plain local storage.

## Response style for Claude Code

When presenting work to the user:

1. Summarize what changed and why.
2. List files touched.
3. Report validation commands run and their results.
4. Call out any remaining risks, platform-specific testing needed, or follow-up build requirements.
5. Keep recommendations specific to the current project rather than giving generic mobile advice.

