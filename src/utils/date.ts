const MONTHS = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

/**
 * Format a post date as "February 22, 2017", matching the legacy Pelican
 * `blog_date_format` filter (no leading zero on the day).
 *
 * Uses UTC accessors so a date stored as midnight UTC does not drift a day
 * backward in negative-offset timezones.
 */
export function formatBlogDate(date: Date): string {
  return `${MONTHS[date.getUTCMonth()]} ${date.getUTCDate()}, ${date.getUTCFullYear()}`;
}

/** Zero-padded year/month/day parts for building `/blog/YYYY/MM/DD/` URLs. */
export function dateParts(date: Date): { year: string; month: string; day: string } {
  return {
    year: String(date.getUTCFullYear()),
    month: String(date.getUTCMonth() + 1).padStart(2, "0"),
    day: String(date.getUTCDate()).padStart(2, "0"),
  };
}

/** The canonical post URL: /blog/YYYY/MM/DD/slug/ */
export function postUrl(date: Date, slug: string): string {
  const { year, month, day } = dateParts(date);
  return `/blog/${year}/${month}/${day}/${slug}/`;
}
