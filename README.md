# pedro.ai — academic website

Pedro Rodriguez's academic site (https://www.pedro.ai), built with
[Astro](https://astro.build) + React + Tailwind CSS v4, matching the
[photography site](https://photography.pedro.ai).

## Develop

```bash
npm install
npm run dev      # local dev server
npm run build    # build static site to dist/
npm run preview  # preview the built site
```

## Structure

- `src/pages/` — routes (file-based). Blog posts are generated at
  `/blog/YYYY/MM/DD/slug/` by `src/pages/blog/[year]/[month]/[day]/[slug].astro`
  from each post's frontmatter `date` + `slug`. Content pages render at
  `/{slug}/` via `src/pages/[slug].astro`.
- `src/content/blog/` — blog posts (Markdown; code via Shiki, math via KaTeX).
- `src/content/pages/` — content pages (`about.md` has `slug: home` → `/`).
- `src/data/publications.ts` — generated from `publications.bib` by
  `scripts/generate_publications.py`.
- `src/layouts/`, `src/components/`, `src/config/nav.ts` — layout, navbar,
  theme toggle, etc.
- `public/` — static assets served verbatim (`/static/**`, `/cv.pdf`,
  `favicon.ico`, `_redirects`, `CNAME`).

URLs intentionally match the previous Pelican site for SEO; `trailingSlash` and
`build.format: 'directory'` in `astro.config.mjs` preserve trailing-slash
directory URLs. Old-domain 301 redirects live in `public/_redirects`.

## Deploy

Netlify (`netlify.toml`): `npm run build` → publish `dist/`.

## Regenerate publications

```bash
python3 scripts/generate_publications.py   # publications.bib -> src/data/publications.ts
```
