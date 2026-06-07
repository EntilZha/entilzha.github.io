// Single source of truth for site navigation, shared by Navbar + footer.
// Kept deliberately focused/professional: About, Blog, Publications.
// Other pages (research projects, violin, recruiting, tips) stay live at their
// URLs and are reached via in-page links rather than the top nav.

export interface NavItem {
  name: string;
  href: string;
}

/** Top-level links shown in the navbar. "About" is the home page (/). */
export const primaryNav: NavItem[] = [
  { name: "About", href: "/" },
  { name: "Blog", href: "/blog/" },
  { name: "Publications", href: "/publications/" },
];

/** Standalone photography site (separate project). */
export const photographyUrl = "https://photography.pedro.ai";

/** Personal (non-professional) links, grouped under a "Personal" dropdown. */
export interface PersonalItem extends NavItem {
  description: string;
  external?: boolean;
}
export const personalNav: PersonalItem[] = [
  {
    name: "Photography",
    href: photographyUrl,
    description: "Nature & wildlife photography",
    external: true,
  },
  {
    name: "Violin",
    href: "/violin/",
    description: "Performances & composing",
  },
];
