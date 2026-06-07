import { useState } from "react";

interface Props {
  bibtex: string;
  defaultOpen?: boolean;
}

export default function BibtexEntry({ bibtex, defaultOpen = false }: Props) {
  const [open, setOpen] = useState(defaultOpen);
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(bibtex);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* clipboard unavailable; ignore */
    }
  };

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="text-xs font-semibold text-cyan-700 hover:underline cursor-pointer"
        aria-expanded={open}
      >
        [{open ? "hide bibtex" : "bibtex"}]
      </button>
      {open && (
        <div className="relative mt-2 w-full max-w-full">
          <button
            type="button"
            onClick={copy}
            className="absolute top-2 right-2 z-10 rounded border border-gray-300 bg-white px-2 py-1 text-xs font-medium text-gray-600 hover:bg-gray-50 cursor-pointer"
          >
            {copied ? "Copied!" : "Copy"}
          </button>
          <pre className="max-w-full overflow-x-auto rounded-lg border border-gray-200 bg-gray-100 p-4 pr-16 text-xs leading-relaxed text-gray-800">
            <code>{bibtex}</code>
          </pre>
        </div>
      )}
    </>
  );
}
