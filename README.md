# CHICC Jewellery

A complete, static front-end website for **CHICC**, a fictional modern European fine jewellery maison. Pure HTML/CSS/JS — no build step, no framework, no server required.

## Running locally

Any static file server works, e.g.:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/index.html
```

Opening `index.html` directly via `file://` also works, but a local server is recommended so relative fetches behave exactly as they will in production.

## Deploying

**Vercel** — import the repository at [vercel.com/new](https://vercel.com/new). No framework preset, no build command, no output directory override needed; it's a static site. Vercel will serve the files as-is.

**GitHub Pages** — push this repository to GitHub, then enable Pages for the `main` branch (root). All links are relative, so it works whether the site is served from a custom domain or a `/reponame/` project path.

## Project structure

```
index.html          Homepage — hero, benefits, collections, Maison editorial, New In
rings.html           }
necklaces.html        }  Category catalogue pages — filters, sort, product grid
earrings.html          }
bracelets.html        }
product.html         Product detail page (data-driven via ?id=)
wishlist.html         Saved-items page (reads localStorage)
maison.html          Maison CHICC story, High Jewellery, commitments
contact.html          Client Service / enquiry / private appointment
styles.css            Full design system (tokens, layout, responsive)
script.js             All interactivity (see below)
products.js           Single source of truth for every product & collection
assets/
  branding/            Logo mark + favicon
  hero/                 Homepage hero artwork (3 slides)
  collections/           Collection card artwork (Éclat, Azure, Lumière, Muse)
  editorial/             Maison CHICC storytelling artwork
  products/
    rings/ necklaces/ earrings/ bracelets/   2 images per product
tools/                Authoring scripts used to generate the artwork, HTML
                       and to QA the build (not required to host the site —
                       see "Regenerating artwork or pages" below)
```

## Product data

Every product lives once, in `products.js`, as a plain object:

```js
{
  id: "r001",
  name: "Éclat Solitaire Ring",
  category: "rings",
  collection: "Éclat",
  material: "White Gold",
  gemstone: ["Diamond"],
  description: "...",
  images: ["assets/products/rings/r001-1.svg", "assets/products/rings/r001-2.svg"],
  featured: true,
  new: true,
  sortOrder: 1
}
```

Every page (category grids, New In, search, related products, the product detail page) renders from this one array, so a category can never accidentally show another category's products, and editing a product only ever means editing one object. 36 products ship in total — 9 each across Rings, Necklaces, Earrings and Bracelets — spanning all four materials (white/yellow/rose gold, platinum), six gemstones (diamond, sapphire, emerald, ruby, pearl, onyx and morganite) and six collections (Éclat, Azure, Lumière, Muse, Nocturne, Rosée).

To add a product: append an object to `CHICC_PRODUCTS` in `products.js` with two images at the referenced paths. No other file needs to change.

## Functionality

- **Wishlist** — heart icon on every card and the product page, persisted in `localStorage`, header count badge, dedicated `wishlist.html`.
- **Search** — full-screen overlay, live filtering across name/category/collection/material/gemstone.
- **Filters & sort** — category pages filter by material, gemstone and collection (checkboxes, AND-combined) and sort by Featured / Newest / Name A–Z / Name Z–A. Reset restores the full set. Filters are also deep-linkable, e.g. `rings.html?collection=eclat` (used by the homepage collection cards).
- **Product detail** — thumbnail gallery, accordions (Details / Gemstone / Craftsmanship / Delivery & Returns), Enquire for Price + Book a Private Appointment.
- **Enquiry & appointment modals** — front-end only (see below), auto-populate the piece name, validate required fields, show a confirmation state on submit.
- **Mobile** — hamburger menu, filter drawer, single/double-column grids, no horizontal scroll, tested at 1440/1280/1024/768/430/390px.
- **Accessibility** — semantic HTML, real `<button>`/`<a>` elements, labelled form fields, Escape closes any open menu/modal/search/drawer, focus moves into opened modals.

No prices are shown anywhere on the site by design — every product surfaces "Enquire" / "Enquire for Price" instead, consistent with CHICC's positioning.

### Wiring up a real backend for enquiries/appointments

Both forms submit through one handler in `script.js` (`initModals`) that currently just shows the confirmation state and logs the payload. To connect a real backend, replace the body of that submit handler with a `fetch()` to your endpoint (or a provider like Formspree/Resend) — the `FormData` field names already match the labelled inputs, so no HTML changes are needed.

## A note on the imagery

Every image on the site — hero artwork, collection cards, and all 72 product photographs — is **original vector artwork generated for this build**, not photography. This was a deliberate substitution, not an oversight: the sandbox this project was authored in has network egress limited to package registries (npm/pip/etc.), so stock photo CDNs (Unsplash, Pexels, and similar) and general web fetches were unreachable, and it was not possible to license or download real photographs of jewellery or a model. Rather than ship broken image links or blurry placeholders, `tools/generate_assets.py` procedurally renders each piece as a clean, on-brand SVG "catalogue" composition — sharp at any zoom, correctly aspect-ratioed, isolated on a soft ivory ground, and colour-accurate to the stated metal and gemstone.

To swap in real photography: replace the files under `assets/products/<category>/`, `assets/hero/`, `assets/collections/` and `assets/editorial/` with photographs of the same filenames and aspect ratio (product shots are 4:5, hero is roughly 18:12.5), or update the paths in `products.js`. No HTML/CSS/JS changes are required — every `<img>` already points at these paths by filename, not by content.

## Regenerating artwork or pages

Everything in `tools/` is optional authoring tooling, kept for anyone who wants to extend the catalogue — it is not required to host the site.

```bash
python3 tools/generate_assets.py   # regenerates assets/*.svg + products.js from the product list in the script
python3 tools/build_html.py        # rebuilds every .html page from the shared header/footer/modal partials
node tools/qa.js                   # headless-browser QA: console/network errors, broken images, filters,
                                    # sort, accordions, modals, wishlist persistence, search, and layout at
                                    # every required breakpoint (needs a local static server running)
```

## Browser support

Built and tested against current Chromium. Uses only standard CSS (Grid, custom properties, `aspect-ratio`) and vanilla JS (no dependencies, no transpilation) — no known issues on current Chrome, Safari, Firefox or Edge.

---

© 2026 CHICC Jewellery. A fictional brand created for this project.
