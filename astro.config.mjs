// @ts-check
import { defineConfig } from 'astro/config';

import react from '@astrojs/react';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.pedro.ai',

  // Preserve the legacy Pelican URL shape: every route is emitted as
  // `<route>/index.html` and served with a trailing slash. This is load-bearing
  // for SEO — do not change without a redirect strategy.
  trailingSlash: 'always',
  build: { format: 'directory' },

  integrations: [react(), sitemap()],

  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
    shikiConfig: {
      theme: 'github-light',
      wrap: true,
    },
  },

  vite: {
    plugins: [tailwindcss()],
  },
});
