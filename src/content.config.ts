import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    slug: z.string(),
    author: z.string().default("Pedro Rodriguez"),
    description: z.string().optional(),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: "*.md", base: "./src/content/pages" }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    author: z.string().default("Pedro Rodriguez"),
    description: z.string().optional(),
    template: z.string().optional(),
  }),
});

export const collections = { blog, pages };
