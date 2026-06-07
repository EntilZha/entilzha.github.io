import { useState, useEffect } from "react";

interface Props {
  src: string;
  full: string;
  alt: string;
}

export default function ProfilePhoto({ src, full, alt }: Props) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onEsc = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    document.addEventListener("keydown", onEsc);
    return () => document.removeEventListener("keydown", onEsc);
  }, []);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="View full photo"
        className="group relative shrink-0 cursor-zoom-in rounded-full focus:outline-none"
      >
        <img
          src={src}
          alt={alt}
          className="h-48 w-48 rounded-full object-cover ring-2 ring-gray-200 shadow-md transition group-hover:ring-cyan-400"
        />
        <span className="pointer-events-none absolute inset-0 rounded-full bg-black/0 transition group-hover:bg-black/10" />
      </button>

      {open && (
        <div
          onClick={() => setOpen(false)}
          className="fixed inset-0 z-[10000] flex cursor-zoom-out items-center justify-center bg-black/85 p-4"
          role="dialog"
          aria-modal="true"
        >
          <img
            src={full}
            alt={alt}
            className="max-h-[92vh] max-w-[92vw] rounded-lg shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          />
          <button
            type="button"
            onClick={() => setOpen(false)}
            aria-label="Close"
            className="absolute top-4 right-4 rounded-full bg-white/10 p-2 text-white hover:bg-white/20"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="h-6 w-6">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}
    </>
  );
}
