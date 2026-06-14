# Source Material for an Expo + Beautiful Mobile UI SKILL.md (June 2026)

## TL;DR

- As of June 2026, the baseline is **Expo SDK 54** (stable, the recommended production baseline with iOS 26 Liquid Glass support) with **SDK 56** in beta; the **New Architecture is mandatory** (React Native 0.85 removed the legacy bridge entirely in April 2026), **Hermes is the default engine**, **Expo Router** is the default file-based router, and **EAS** is the canonical build/update/submit pipeline.
- The opinionated modern stack: **Expo Router + TypeScript + NativeWind or Unistyles 3 for styling + Reanimated 4 + Gesture Handler for animation + FlashList v2 for lists + expo-image + TanStack Query (server state) + Zustand (client state) + Sentry + Maestro (E2E)**, all on development builds rather than Expo Go for production work.
- “Beautiful and innovative” comes from native feel, not decoration: UI-thread animations at 60/120fps, spring physics, haptics on key interactions, platform-correct navigation, safe-area/edge-to-edge handling, skeletons over spinners, and avoiding the “AI-generated” tells (purple gradients, Inter everywhere, identical shadows, emoji-as-icons).

## Key Findings

### 1. Expo Core Architecture & Setup

**SDK versions and cadence.** Expo releases roughly three SDKs per year. As of June 2026, **SDK 54** is the stable production baseline (it shipped iOS 26 Liquid Glass support, Android edge-to-edge by default, and precompiled React Native for faster iOS builds), and **SDK 56 is in beta** (announced May 2026 with Hermes V1 default, stable Expo UI, and Expo Router forked from React Navigation). Per the official Expo SDK 56 changelog, a new Kotlin compiler plugin “replaces reflection with build-time code generation for Expo Modules on Android,” yielding “roughly 40% faster cold starts and 33% faster first render, with no app-side changes required”  (Expo reported Activity.onCreate dropping 93ms→55ms and Time-to-Interactive 797ms→531ms),  and Expo’s May 2026 launch post advertised “50%+ faster iOS builds (precompiled XCFrameworks)”  (the GA changelog more conservatively cites iOS clean builds ~16% faster plus another ~20% on EAS from precompiled community libraries). **Always upgrade one SDK at a time** — never jump multiple versions; run `npx expo install --fix` and the relevant codemods. Use `npx expo install` (not raw npm/yarn) to keep dependency versions aligned with the SDK.

**The New Architecture (mandatory in 2026).** The New Architecture = **JSI** (direct C++ refs replacing the JSON bridge) + **Fabric** (concurrent renderer in C++) + **TurboModules** (lazily-loaded, type-safe native modules) + **Codegen** + **Bridgeless mode**. It became the default in RN 0.76, the only option in 0.82, and the legacy bridge was deleted entirely in RN 0.85 (April 2026). Per Expo’s official New Architecture docs, “As of January 2026, approximately 83% of SDK 54 projects built with EAS Build use the New Architecture.”  Reported real-world gains: faster cold starts, faster rendering, lower memory. Practical implications: **all libraries must be New-Arch compatible** (audit via React Native Directory + `npx expo-doctor`); Reanimated 4, FlashList v2, and Unistyles 3 are New-Arch-only. Hermes is required.

**Expo Router (file-based routing).** Routes derive from the `app/` (or `src/app/`) directory. Best practices:

- Use **typed routes** (`experiments.typedRoutes: true`) for autocomplete and refactor-safety; absolute paths only (no relative `./about`).
- Use **route groups** `(group)` to organize without affecting URLs, e.g. `(auth)` and `(app)`/`(tabs)`.
- Layouts (`_layout.tsx`) are just React components — wrap providers (auth, query client, theme) at the root layout.
- **Protected routes**: the modern declarative pattern is `<Stack.Protected guard={isLoggedIn}>` (also `Tabs.Protected`).  Guards are evaluated client-side, redirect to the anchor/first available route, and crucially **are enforced even on deep links** (an unauthenticated deep link to a protected modal redirects to sign-in).  When `isLoggedIn` changes the layout re-renders and auto-navigates.  This replaces the older imperative `<Redirect>`/`useEffect` redirect hacks (which were fragile against deep links and race conditions).
- Persist auth via a context provider backed by `expo-secure-store` (native) / `localStorage` (web).
- In SDK 56+, Expo Router no longer re-exports `@react-navigation/*`; repoint imports to `expo-router` entry points (there’s a codemod).
- File-based routing gives automatic deep linking, async route bundle-splitting, and static web rendering (SEO).

**EAS Build / Submit / Update.**

- **Build profiles** live in `eas.json` (default: `development`, `preview`, `production`); `development` sets `developmentClient: true` + `distribution: internal`.  Use `extends` to share config (up to 5 deep).  Build caching can speed builds up to ~30%. 
- **Environment variables**: the EAS environment-variable system (development/preview/production environments) is the single source of truth, with three visibility tiers — **plain text**, **sensitive**, and **secret** (secret never leaves EAS servers, can’t be pulled or embedded in OTA updates).  `EXPO_PUBLIC_`-prefixed vars are embedded in the JS bundle (never put secrets there). Set `environment` explicitly per build profile. **Breaking change in SDK 55+**: `eas update` now *requires* the `--environment` flag (previously defaulted to `.env`); CI pipelines that omit it will fail.
- **EAS Update (OTA)**: channels map to build profiles; push JS/asset changes that don’t touch native code, bypassing app-store review. Use **staged rollouts** (`--rollout-percentage`), monitor, then expand; `eas update:republish` to roll back. Critical rule: OTA can only update JS/assets, not native code — a native dependency change requires a new build.
- **EAS Workflows** is the recommended CI/CD (GitHub build triggers are being deprecated). Authenticate CI with `EXPO_TOKEN`.

**CNG / prebuild / config plugins.** With **Continuous Native Generation**, the `ios/` and `android/` folders are *generated, not maintained* — describe native config declaratively in `app.json`/`app.config.ts` + **config plugins**, and run `npx expo prebuild` (or let EAS do it). Delete native folders before regenerating on upgrade. This eliminates merge conflicts in native code  and makes upgrades far easier. Prefer `app.config.ts` for dynamic/typed config. Avoid committing generated native folders when using CNG.

**Development builds vs Expo Go.** Use **Expo Go** only for quick prototyping/learning (it only supports the latest SDK and the bundled set of native modules). Use **development builds** (`expo-dev-client`) for any real/production app — they support custom native code, config plugins, and have much longer EAS backwards compatibility.

**Project structure / monorepo.** Feature-oriented structure is the community norm (e.g., Obytes starter: each feature self-contained with screens, components, API, state). Respected starters: **Obytes** (Expo + PNPM + TS + Tailwind/NativeWind + expo-router + react-query + react-hook-form + EAS + GitHub Actions; “minimal code and dependencies,” strong CI defaults), **Ignite (Infinite Red)** (mature, generators, New Arch on by default), and **create-expo-stack** (configurable scaffolder). Monorepos typically use PNPM workspaces or Nx.

### 2. Styling & UI Component Stacks

**StyleSheet still works** — it’s fast, zero-setup, and fine for small apps; but a large share of RN developers use something else because it lacks theming, variants, responsive tokens, and causes re-renders for dynamic styles.

**The three leading solutions in 2026 (NativeWind, Unistyles, Tamagui) are a team/philosophy choice, not a pure performance one:**

- **NativeWind** (Tailwind for RN) — by far the most popular (per npm trends, June 2026: ~942,000 weekly downloads and ~7,800 GitHub stars for v4.2.x). Compiles Tailwind classes to `StyleSheet.create` objects at build time.  Best for teams who know Tailwind / want web+native parity; underpins gluestack-ui v3 and react-native-reusables. Current major version is v4.
- **Unistyles 3** (`react-native-unistyles`) — a **superset of StyleSheet built in C++/JSI with Nitro Modules**, tightly integrated with Fabric and the Shadow Tree. Its killer feature is **selective updates with zero re-renders**: it builds a C++ representation of your styles and their dependencies (it can track up to 16: theme, breakpoints, variants, color scheme, insets, IME/keyboard height, etc.) and mutates the shadow tree directly, “adding under 0.1ms” to a stylesheet. New-Architecture-only. Best when you want StyleSheet familiarity + performance + powerful theming and don’t mind native dependency. (Caveat: native updates can’t ship via OTA — needs a full build.) Unistyles 2.x support ended Dec 31, 2025.
- **Tamagui** — UI kit + **optimizing compiler** that flattens component trees at build time → atomic CSS on web, plain Views on native; near-zero runtime overhead and excellent benchmark scores. Best for universal web+native with a strict design-token system.  Trade-offs: steep setup (compiler + bundler/Babel config) and docs that are hard to follow (theming specifically criticized).
- Shopify **Restyle** also benchmarks very well and is the pick for TypeScript-enforced design systems (type-safe tokens, no magic numbers).

**Component libraries:**

- **gluestack-ui v3** (successor to the now-deprecated NativeBase, 2023) — unstyled accessible primitives styled with NativeWind/Tailwind, copy-paste or CLI; optimized for SDK 54 + New Arch; accessibility built on `@react-native-aria`.  Pick for full accessibility with minimal work.
- **react-native-reusables** (“shadcn for RN”, ~8.2k stars, active) — copy-paste/registry model on NativeWind + RN Primitives (universal Radix port) + Reanimated + Lucide.  You own the code; smallest bundle impact; strongly Expo-associated. Pick for the shadcn ownership model + max customization.
- **React Native Paper** (maintained by Callstack; per npm trends, ~372,000 weekly downloads and ~14,300 GitHub stars for v5.15.x) — the most reliable **Material Design 3** implementation, best-in-class accessibility OOTB (48×48dp targets). Pick for Material/Android-first.
- **Tamagui** also ships a component kit.
- **NativeBase is deprecated** — migrate to gluestack v3. React Native Elements is declining (legacy only); UI Kitten maintenance has slowed.
- **Expo UI** (stable in SDK 56, beta in 54+) is *not* a styled UI kit — it exposes **real SwiftUI (iOS) and Jetpack Compose (Android) primitives** to React with 1-to-1 mapping. Use it for truly native pickers/switches/sliders/menus and for iOS 26 effects (glass, mesh gradients).

**Design tokens / theming / dark mode.** Centralize a theme object (colors, spacing, typography, radii) and reference tokens everywhere — never scatter hex/magic numbers. Use `useColorScheme()` for light/dark; wrap with `ThemeProvider` (Expo Router exports `DarkTheme`/`DefaultTheme`). Unistyles and Restyle make dynamic theming/dark mode a single switch. For iOS 26 Liquid Glass, colors must use `PlatformColor`/`DynamicColorIOS` since glass auto-adapts to light/dark backgrounds.

**Responsive / safe area / notch.** Use **`react-native-safe-area-context` 5.x** via the **`useSafeAreaInsets()` hook** — both Expo and React Navigation explicitly recommend it over RN’s built-in `SafeAreaView`  (now deprecated). Don’t wrap the whole app in one SafeAreaView (wastes space)  — apply insets per-edge/per-element. **Android 15 (API 35) forces edge-to-edge**  (and Expo SDK 54 enables it for all Android apps, non-disableable),  so content draws behind system bars and you must inset it; hardcoded status-bar padding now overlaps system chrome. safe-area-context 5.x also tracks IME/keyboard insets. 

### 3. Animation & Interaction (the “beautiful UI” core)

**Reanimated 4** (stable mid-2025, New-Architecture/Fabric-only; requires RN 0.76+). Two complementary systems:

- **CSS-style animations & transitions** (new) — declarative, web-familiar `transitionProperty`/`transitionDuration`/`animationName` style props; recommended for the ~80% of animations that are **state-driven** (modals, tooltips, accordions, color/opacity changes).
- **Worklets + shared values** (the proven engine) — imperative, frame-level control; recommended for the ~20% that need gestures, scroll-linked effects, screen transitions, or orchestrated sequences.
- All animations run on the **UI thread**, so they stay smooth even when the JS thread is blocked. Worklets were extracted into a separate **`react-native-worklets`** package; Babel config changes from `react-native-reanimated/plugin` to `react-native-worklets/plugin`  (must be last). The v3→v4 API is backward compatible — minimal/no code changes once you’re on New Arch. Reanimated can animate every prop at up to 120fps. 
- **Prefer spring physics** (`withSpring`) over linear timing for natural motion; use `withDecay` to preserve gesture velocity/momentum on release. 

**Gesture Handler** runs gesture recognition on the UI thread using native recognizers and composes via the `Gesture` API (`GestureDetector`); pairs directly with Reanimated. Drop `PanResponder` for anything new. Maintain `testID`/accessibility-label discipline (also used by Maestro).

**Skia (`@shopify/react-native-skia`, latest 2.6.x, RN 0.79+/React 19, Expo SDK 55+).** A GPU-accelerated 2D engine (same engine behind Chrome/Android/Flutter) for **custom graphics**: charts with thousands of points at 60fps, shaders (SKSL), blurs, image filters, gradients, procedural textures, page-curl/creative effects. It’s a *second rendering path* — keep navigation/lists/forms as normal Views, use Skia as a leaf canvas. It accepts Reanimated shared values **directly** as props (no `createAnimatedComponent`), reading them on the UI thread each frame. Cost: adds ~3–5MB to the binary; for plain icons/static SVG, `react-native-svg` is lighter.

**Lottie / Rive.** Use `lottie-react-native` for designer-authored vector animations; **Rive** for interactive/state-machine-driven vector animations (smaller files, runtime state control).

**Haptics (`expo-haptics`).** A top “secret ingredient” of native feel. Use `impactAsync` (Light/Medium/Heavy), `notificationAsync` (success/warning/error), `selectionAsync`. Best moments: successful submission, toggles, payment confirmation, likes/follows, reaching breakpoints. **Don’t overuse** — excessive haptics annoy users and drain battery;  respect system settings.

**60/120fps best practices.** Keep animation/layout work off the JS thread (Reanimated/Gesture Handler, or `useNativeDriver: true` for legacy Animated opacity/transform only — it can’t animate width/height/margin). Use the Perf Monitor to watch **UI-thread FPS** (animations) vs **JS-thread FPS** (renders). Avoid driving pressed/hover state through `setState` (pay a React render tick) — use Reanimated/Pressable.

### 4. Mobile UI/UX Design Principles & Innovation

**Platform divergence is the defining 2026 design reality.** Apple’s **Liquid Glass** (iOS 26, the biggest redesign since iOS 7 — translucent material that refracts/reflects in real time across controls, tab bars, sheets) and Google’s **Material 3 Expressive** (Android 16 — bold saturated color, variable typography, springy elastic motion, heavy background blur, large pill controls) have pulled the platforms apart. **Recommendation: adapt to each platform’s conventions rather than inventing one cross-platform look** — most users only use one platform and expect its native patterns; a bespoke identical-everywhere UI reads as foreign. Use platform-native components/navigation. (Caveat: critics note both Liquid Glass and Expressive can hurt legibility/accessibility — provide Reduce Transparency / high-contrast fallbacks; iOS exposes `AccessibilityInfo.isReduceTransparencyEnabled()`.)

**Implementing Liquid Glass in Expo:** four paths — (1) `expo-glass-effect` `GlassView`/`GlassContainer` (UIKit `UIVisualEffectView`, iOS 26+, falls back to plain View; check `isLiquidGlassAvailable()` at runtime; don’t animate opacity to 0); (2) `@expo/ui` SwiftUI `glassEffect` modifier; (3) Expo Router **native tabs** (`expo-router/unstable-native-tabs`) for system liquid-glass tab bars; (4) Callstack `@callstack/liquid-glass`. Reserve glass for top-level interaction surfaces (nav/tab bars), let content run edge-to-edge behind it, keep hierarchy in layout/spacing not decorative layers, keep labels high-contrast in all modes, and avoid full-screen glass sheets.

**Typography & fonts (`expo-font`).** Two methods: the **config plugin** (recommended for native — embeds fonts at build time, available immediately, no flash) or the **`useFonts` hook** (runtime, works on web). Keep splash up via `SplashScreen.preventAutoHideAsync()` until fonts/critical assets are preloaded to avoid flicker. Limit weights (2–3 is plenty); one base + one heading family. Expo officially supports OTF/TTF; **variable fonts lack full cross-platform support** — use static cuts (or extract axes with fontTools). Use typographic craft (letter-spacing tiers) to make even system fonts feel intentional.

**Color & accessibility.** Don’t rely on color alone (add text/icon/pattern). Honor dynamic type / font scaling, dark mode, and **Reduce Motion** (gate animations on `AccessibilityInfo.isReduceMotionEnabled()` — ignoring it is a genuine accessibility failure). Set `accessibilityLabel` on all touchables (don’t rely on auto-labels), `accessibilityRole`, `accessibilityState`; **minimum 44×44pt touch targets** (WCAG 2.5.5 / Apple HIG) — use `hitSlop` or padding for small icons; manage focus after navigation/modal/content changes; announce dynamic changes via `AccessibilityInfo.announceForAccessibility()`. Hide decorative elements (`accessibilityElementsHidden` iOS / `importantForAccessibility="no-hide-descendants"` Android). Lint with `eslint-plugin-react-native-a11y`; test with VoiceOver (physical iOS device) and TalkBack.

**Layout / navigation patterns.** Respect thumb zones (primary actions in reach). Tab bars + stacks (nest a stack inside a tab), modals, and **bottom sheets** are the core patterns. Use native-stack for screen transitions (40–60% fewer dropped frames vs JS stack). Enable `lazy` + `detachInactiveScreens` on tab navigators.

**States.** Use **skeleton screens over spinners** (“spinners scream loading; skeletons whisper almost ready”); design real **empty states** and **error states**; use **optimistic UI** for instant-feeling mutations.

**What makes UI feel “native”/polished vs generic/AI-generated.** DO: native components + momentum scrolling, platform-correct navigation, UI-thread animations at 60/120fps, spring physics, haptics on key actions, instant touch feedback (<100ms) with hit-slop, skeletons + preloaded splash, safe-area/edge-to-edge, depth hierarchy via *varied* shadows, dark-mode/reduced-motion/font-scaling support. The **“AI-generated/vibe-coded” tells**: purple→indigo gradients  on white (a bias that traces directly to Tailwind — creator Adam Wathan publicly joked in Aug 2025, “I’d like to formally apologize for making every button in Tailwind UI ‘bg-indigo-500’ five years ago,”  and Cursor’s Head of Design Ryo Lu dubbed the resulting look “AI slop”), default fonts (Anthropic’s own frontend-design skill instructs: “NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds)”),  the *same shadow on every element* (kills depth), emoji-as-UI-icons,  glassmorphism everywhere, everything-in-cards, bounce/elastic easing, web-like hover states on touch, no haptics, janky JS-thread/30fps animations, generic placeholder content, missing empty/loading/error states, and an “averaged,” point-of-view-less look. (Several of these come from practitioner blogs — corroborated across multiple sources and aligned with Software Mansion/Callstack/Expo official guidance.)

### 5. Performance & Quality

**Lists: FlashList v2 over FlatList.** `@shopify/flash-list` v2 was rebuilt for the New Architecture (New-Arch-only, JS-only, no native deps); it **recycles components** instead of unmount/remount, **no longer needs `estimatedItemSize`** (auto-sizes), supports masonry, `getItemType` recycling pools, and maintain-visible-content-position. Reported 5–10x gains on large/complex lists, especially low-end Android; teams have seen JS-thread CPU drop from >90% to <10%. Use FlatList for small lists (<~200–300 items). LegendList is a newer Fabric/Reanimated-based alternative. For custom-rendered content, Skia’s experimental SkiaList hits 120fps.

**Images (`expo-image`).** Replace RN `Image`: built-in disk/memory caching (`cachePolicy`), `placeholder` with **blurhash/thumbhash** for immersive progressive loading, `transition` for fade-in, `contentFit`, and `allowDownscaling` to cut memory. Serve correctly-sized images from a CDN. Preload critical assets with `expo-asset` / `Image.prefetch` behind the splash.

**Bundle/startup.** Hermes (default) gives faster startup + lower memory + AOT bytecode. Lazy-load screens/heavy deps; trim dependencies; use Expo Atlas to inspect the bundle. Toggle-check Hermes after native config regeneration.

**State management — the layered 2026 consensus:** **TanStack Query** for *server state* (caching, refetch, dedup, optimistic updates — ~80% of what most apps call “state”); **Zustand** for *client/global UI state* (~1–3KB, no provider, no boilerplate; the dominant dedicated store — npm trends shows ~36.6M weekly downloads and ~58k GitHub stars for v5.0.x, far ahead of alternatives); **Jotai** for fine-grained atomic/derived state; React **Context** only for low-frequency global values (theme, auth) — it re-renders all consumers; component-local `useState`/`useReducer` for the rest. **Redux Toolkit** only for large teams needing strict patterns/time-travel. Persist Zustand with the `persist` middleware (MMKV is a fast storage backend). Use Zustand **selectors** (not destructuring) to avoid spurious re-renders. Forms: **React Hook Form + Zod**.

**Offline-first.** TanStack Query cache persistence + MMKV/SQLite; `expo-sqlite` (with new object-oriented APIs) for local data.

**Avoiding re-renders (the #1 RN perf problem).** Memoize components (`React.memo`), stabilize callbacks (`useCallback`) and objects/arrays (`useMemo`); don’t define components/styles/handlers inline in `renderItem` or JSX; use stable keys; lift/colocate state so only what changed re-renders; use `useRef` for values that shouldn’t trigger renders. Profile with **React DevTools Profiler** (“Highlight updates”) and the Perf Monitor. (Flipper is largely deprecated in favor of the new Hermes debugger / React Native DevTools.) **Don’t over-optimize a pre-launch app** — ship, then profile the real bottleneck.

**Testing.** **Jest + React Native Testing Library** for unit/component (testing pyramid ~70/20/10). For **E2E**, **Maestro** is the 2026 default for most teams — YAML flows, no native build changes, reusable sub-flows, auto-retry/tolerance, fast iteration; **Detox** wins only for pure-RN apps that need the lowest flakiness (gray-box JS-thread sync, <2% flake) but is heavier to set up, iOS-simulator-only, and Wix no longer treats it as a primary project. Both rely on `testID`/accessibility-label discipline. Build Detox binaries via an EAS profile if used.

**TypeScript.** Use throughout (it’s the default template); typed routes, typed env, Zod for runtime validation at boundaries.

### 6. Developer Experience & Tooling

- **Linting/formatting**: ESLint (`eslint-config-expo`) + Prettier is standard; **Biome** is a fast emerging all-in-one alternative. Add `eslint-plugin-react-native-a11y`.
- **Debugging**: `expo-dev-client` dev menu + **React Native DevTools** (Hermes-based; Flipper is deprecated).
- **Common config plugins / native modules**: `expo-camera`, `expo-notifications`, `expo-secure-store`, `expo-image-picker`, `expo-location`, `expo-sqlite`, `expo-haptics`, `expo-av`/`expo-audio`/`expo-video`, `expo-file-system`. Most are added via `npx expo install` + a config plugin entry.
- **Error monitoring**: **Sentry** (`@sentry/react-native`) — upload source maps in a post-build step using a `SENTRY_AUTH_TOKEN` secret env var. Add analytics (e.g., PostHog, Amplitude) and EAS Insights/Expo Observe.
- **CI/CD**: EAS Workflows (or GitHub Actions with `eas-cli` + `EXPO_TOKEN`); webhook build notifications to Slack/Teams; `eas build --local` to reproduce build issues; `npx expo-doctor` as a pre-commit/CI gate.
- **AI agent tooling**: Expo ships official **Expo Skills** (github.com/expo/skills, ~1.7k stars; a Claude Code plugin + Cursor remote-rule install) and exposes docs as markdown (append `.md` to any docs URL) plus `llms.txt`. There’s also an `upgrading-expo` skill. Point agents at versioned docs rather than training data.

### 7. Common Pitfalls & Anti-Patterns

- **Using Expo Go for a production app** (then hitting the wall on native modules) — use development builds.
- **Jumping multiple SDK versions** at once — upgrade incrementally.
- **Not auditing dependencies for New-Arch compatibility** before upgrading (RN 0.85 has no bridge fallback).
- **Putting secrets in `EXPO_PUBLIC_` vars** (they’re in the JS bundle); forgetting `--environment` on `eas update` in SDK 55+ (CI breaks).
- **Committing CNG-generated `ios`/`android` folders** or editing them by hand instead of using config plugins.
- **Hardcoding status-bar padding** instead of safe-area insets — breaks under Android 15 edge-to-edge and on notch/Dynamic Island devices.
- **FlatList for big/complex lists**; inline functions/objects/components in `renderItem`; unstable keys; wrong/absent `estimatedItemSize` on FlashList v1.
- **Animating on the JS thread** / using Animated without `useNativeDriver` / animating width/height instead of transform/scale; driving touch-feedback state through `setState`.
- **Re-render storms**: Context for high-frequency state; Zustand destructuring instead of selectors; unmemoized callbacks/props.
- **Treating server data as client state** (skip the loading/cache/staleness pain — use TanStack Query).
- **Over-using haptics/animations/glass**; ignoring Reduce Motion / Reduce Transparency / Dynamic Type.
- **iOS vs Android quirks**: Android edge-to-edge & back-gesture, shadow rendering differs (elevation vs shadow*), VoiceOver-only-on-device, font scaling, keyboard avoidance (`behavior="padding"` on Android), liquid-glass dark-mode flicker (wrap layout in `ThemeProvider`).
- **The bottom-sheet/Reanimated-4 caveat**: `@gorhom/bottom-sheet` v5 (the de-facto standard, New-Arch compatible; per npm trends ~1.4–1.6M weekly downloads, ~8.9k stars) historically depended on Reanimated v3 APIs;  verify Reanimated 4 compatibility against your SDK before committing (open issue #2600 as of Jan 2026).  Alternatives: `expo` bottom sheet wrapper, `react-native-true-sheet` (truly native).

## Recommendations

**For a new Expo project (foundation):**

1. Scaffold with `create-expo-app` (TypeScript, Expo Router) on the latest stable SDK (54 now; move to 56 when it’s GA). Enable typed routes. Use `src/app` + feature-oriented folders.
1. Set up **development builds** + `eas.json` with development/preview/production profiles and the EAS environment-variable system from day one. Add `npx expo-doctor` and ESLint/Prettier (or Biome) to CI.
1. Pick a styling stack: **NativeWind** (if you/your team like Tailwind or want web parity) or **Unistyles 3** (if you want max performance + powerful theming with StyleSheet familiarity). Add **gluestack-ui v3** or **react-native-reusables** for components, or **React Native Paper** for Material.
1. Install the core native-feel stack: **Reanimated 4 + Gesture Handler**, **FlashList v2**, **expo-image**, **react-native-safe-area-context 5.x**, **expo-haptics**, **@gorhom/bottom-sheet** (verify Reanimated 4 compat).
1. State: **TanStack Query + Zustand**; forms with **React Hook Form + Zod**; storage via **expo-secure-store** + MMKV/expo-sqlite.
1. Add **Sentry** + analytics + EAS Update channels early.

**For improving an existing codebase (staged):**

1. **Audit & stabilize**: run `npx expo-doctor`, check New-Arch compatibility of every native dep, upgrade SDK one step at a time, ensure Hermes + New Arch are on.
1. **Performance pass**: replace FlatList→FlashList v2, RN Image→expo-image with blurhash, fix re-render storms (memo/selectors/no inline renderItem), move animations to Reanimated/UI thread, native-stack navigation, lazy tabs.
1. **Polish pass**: add haptics on key actions, skeletons over spinners, spring physics, safe-area/edge-to-edge correctness, real empty/error states, optimistic UI.
1. **Accessibility pass**: labels/roles/states, 44×44 targets, Reduce Motion/Transparency, focus management, `eslint-plugin-react-native-a11y`, VoiceOver/TalkBack testing.
1. **Platform pass**: adopt platform-correct navigation and, where it elevates the product, native primitives (Expo UI / native tabs / Liquid Glass on iOS 26, Material 3 on Android).

**Benchmarks/thresholds that change the plan:** target 60fps (120 on capable devices) on UI thread during scroll/animation; cold start under ~2s on mid-tier Android; if a meaningful share of users are on iOS 15.x, delay SDK 56 (drops iOS 15). Don’t optimize below 100 DAU — ship and measure first.

## Caveats

- The ecosystem moves fast: SDK 56, Reanimated 4, FlashList v2, Unistyles 3, and Expo UI all had major changes in the last ~12 months — pin versions and verify against official docs (use the `.md`/`llms.txt` endpoints) before coding.
- Some performance figures (cold-start/render % gains, FlashList 5–10x) come from vendor or practitioner benchmarks, not independent audits — treat as directional. Download/star counts cited are point-in-time npm-trends/GitHub snapshots (June 2026) and drift quickly.
- The `@gorhom/bottom-sheet` ↔ Reanimated 4 compatibility deadlock is the single most important thing to verify against current docs before building.
- Several design “native feel” and “AI-tell” points are practitioner opinion (blogs/Medium), though they recur consistently and align with official Software Mansion/Callstack/Expo guidance.
- Liquid Glass / Material 3 Expressive are new and somewhat controversial on accessibility; always ship reduced-transparency/high-contrast fallbacks.