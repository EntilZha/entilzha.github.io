import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import { postUrl } from "../../utils/date";
import { excerpt } from "../../utils/excerpt";

const SITE = "https://www.pedro.ai";
const FEED_URL = `${SITE}/feeds/all.atom.xml`;

function esc(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// Atom feed at /feeds/all.atom.xml, preserving the legacy Pelican feed URL.
export const GET: APIRoute = async () => {
  const posts = (await getCollection("blog")).sort(
    (a, b) => b.data.date.getTime() - a.data.date.getTime(),
  );

  const updated = (posts[0]?.data.date ?? new Date()).toISOString();

  const entries = posts
    .map((post) => {
      const url = SITE + postUrl(post.data.date, post.data.slug);
      const summary = post.data.description ?? excerpt(post.body ?? "");
      return `  <entry>
    <title>${esc(post.data.title)}</title>
    <link href="${url}" />
    <id>${url}</id>
    <updated>${post.data.date.toISOString()}</updated>
    <published>${post.data.date.toISOString()}</published>
    <author><name>${esc(post.data.author)}</name></author>
    <summary>${esc(summary)}</summary>
  </entry>`;
    })
    .join("\n");

  const xml = `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Pedro Rodriguez</title>
  <subtitle>Writing on machine learning, NLP, software, and the outdoors.</subtitle>
  <link href="${FEED_URL}" rel="self" type="application/atom+xml" />
  <link href="${SITE}/" rel="alternate" type="text/html" />
  <id>${SITE}/</id>
  <updated>${updated}</updated>
  <author><name>Pedro Rodriguez</name></author>
${entries}
</feed>
`;

  return new Response(xml, {
    headers: { "Content-Type": "application/atom+xml; charset=utf-8" },
  });
};
