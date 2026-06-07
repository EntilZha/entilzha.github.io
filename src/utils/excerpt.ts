/**
 * Build a plain-text excerpt from raw markdown, for blog listing previews.
 * Strips code, HTML, images, math, and markdown syntax, then truncates at a
 * word boundary.
 */
export function excerpt(markdown: string, maxChars = 240): string {
  let text = markdown;

  text = text.replace(/```[\s\S]*?```/g, " "); // fenced code blocks
  text = text.replace(/`[^`]*`/g, " "); // inline code
  text = text.replace(/\$\$[\s\S]*?\$\$/g, " "); // display math
  text = text.replace(/\$[^$\n]*\$/g, " "); // inline math
  text = text.replace(/<[^>]+>/g, " "); // html tags
  text = text.replace(/!\[[^\]]*\]\([^)]*\)/g, " "); // images
  text = text.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1"); // links -> text
  text = text.replace(/^\s{0,3}#{1,6}\s+/gm, ""); // heading markers
  text = text.replace(/^\s{0,3}>\s?/gm, ""); // blockquotes
  text = text.replace(/[*_~`]/g, ""); // emphasis / strikethrough
  text = text.replace(/^\s*[-*+]\s+/gm, ""); // list bullets
  text = text.replace(/\s+/g, " ").trim(); // collapse whitespace

  if (text.length <= maxChars) return text;
  const cut = text.slice(0, maxChars);
  const lastSpace = cut.lastIndexOf(" ");
  return (lastSpace > 0 ? cut.slice(0, lastSpace) : cut).replace(/[.,;:]$/, "") + "…";
}
