#!/usr/bin/env python3
"""Assembles every static HTML page from shared header/footer/modal partials
so the markup can never drift between pages. Output is plain static HTML —
no build step is required to host the result on GitHub Pages / Vercel."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def W(path, content):
    with open(os.path.join(ROOT, path), "w") as f:
        f.write(content)


def head(title, desc, active="", body_attrs="", full_title=None):
    page_title = full_title if full_title else f"{title} — CHICC Jewellery"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="assets/branding/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="styles.css">
</head>
<body{(' data-active="' + active + '"') if active else ""}{body_attrs}>
'''


HEADER = '''<a class="visually-hidden" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner container">
    <div class="header-left" style="display:flex;align-items:center;">
      <button type="button" class="burger" data-menu-open aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
        <span></span><span></span><span></span>
      </button>
      <nav class="header-nav left" aria-label="Primary">
        <a class="nav-link" href="rings.html">Rings</a>
        <a class="nav-link" href="necklaces.html">Necklaces</a>
        <a class="nav-link" href="earrings.html">Earrings</a>
        <a class="nav-link" href="bracelets.html">Bracelets</a>
        <a class="nav-link" href="maison.html#high-jewellery">High Jewellery</a>
        <a class="nav-link" href="maison.html">Maison CHICC</a>
      </nav>
    </div>

    <a href="index.html" class="brand-mark" aria-label="CHICC Jewellery — home">
      <img src="assets/branding/mark.svg" alt="" width="26" height="14">
      <span class="word">CHICC</span>
      <span class="sub">JEWELLERY</span>
    </a>

    <div class="header-nav right header-actions">
      <button type="button" class="icon-btn" data-search-open aria-label="Search">''' + "SEARCH_ICON" + '''</button>
      <a class="icon-btn" href="wishlist.html" aria-label="Wishlist">''' + "HEART_ICON" + '''<span class="count" data-wishlist-count style="display:none;"></span></a>
      <a class="icon-btn" href="contact.html#client-services" aria-label="Account &amp; client services">''' + "USER_ICON" + '''</a>
      <div class="header-cta">
        <a class="nav-link enquire-link" href="#" data-enquire-open data-piece="General Enquiry">Enquire</a>
        <a class="nav-link" href="contact.html">Contact</a>
      </div>
    </div>
  </div>
</header>

<div class="mobile-menu" id="mobileMenu">
  <div class="mobile-menu-header container">
    <button type="button" class="icon-btn" data-menu-close aria-label="Close menu">''' + "CLOSE_ICON" + '''</button>
  </div>
  <nav class="mobile-menu-list" aria-label="Mobile primary">
    <a href="rings.html">Rings</a>
    <a href="necklaces.html">Necklaces</a>
    <a href="earrings.html">Earrings</a>
    <a href="bracelets.html">Bracelets</a>
    <a href="maison.html#high-jewellery">High Jewellery</a>
    <a href="maison.html">Maison CHICC</a>
    <a href="#" data-enquire-open data-piece="General Enquiry">Enquire</a>
    <a href="contact.html">Contact</a>
  </nav>
  <div class="mobile-menu-footer">
    <a class="btn btn-outline btn-block" href="wishlist.html">View Wishlist</a>
  </div>
</div>
'''

ICONS = {
    "SEARCH_ICON": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="11" cy="11" r="7.2"/><path d="M21 21l-4.4-4.4"/></svg>',
    "HEART_ICON": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 20.5s-7.5-4.6-10-9.4C.5 7.4 2.6 4 6.3 4c2 0 3.6 1 5.7 3.2C14.1 5 15.7 4 17.7 4c3.7 0 5.8 3.4 4.3 7.1-2.5 4.8-10 9.4-10 9.4Z"/></svg>',
    "USER_ICON": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="8" r="3.6"/><path d="M4.5 20c1.6-3.6 4.6-5.4 7.5-5.4s5.9 1.8 7.5 5.4"/></svg>',
    "CLOSE_ICON": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M5 5l14 14M19 5L5 19"/></svg>',
}
for k, v in ICONS.items():
    HEADER = HEADER.replace(k, v)

FOOTER = '''<footer class="site-footer">
  <div class="container">
    <div class="footer-brand">
      <div class="word">CHICC</div>
      <div class="sub">JEWELLERY</div>
    </div>
    <div class="footer-grid">
      <div class="footer-col">
        <h4>Collections</h4>
        <a href="rings.html">Rings</a>
        <a href="necklaces.html">Necklaces</a>
        <a href="earrings.html">Earrings</a>
        <a href="bracelets.html">Bracelets</a>
        <a href="maison.html#high-jewellery">High Jewellery</a>
      </div>
      <div class="footer-col">
        <h4>Maison</h4>
        <a href="maison.html">Maison CHICC</a>
        <a href="contact.html">Contact</a>
        <a href="contact.html#appointment">Private Appointment</a>
      </div>
      <div class="footer-col">
        <h4>Client Services</h4>
        <a href="maison.html#care">Lifetime Care</a>
        <a href="maison.html#sourcing">Ethical &amp; Conflict-Free Sourcing</a>
        <a href="maison.html#craftsmanship">Expert Craftsmanship</a>
        <a href="contact.html#client-services">Private Client Service</a>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <p>Client Service<br>+33 1 42 00 00 00</p>
        <p>hello@chicc-jewellery.com</p>
        <p>By appointment only</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 CHICC Jewellery</span>
      <div class="legal-links">
        <a href="#">Privacy</a>
        <a href="#">Terms</a>
      </div>
    </div>
  </div>
</footer>
'''

MODALS = '''
<!-- Search overlay -->
<div class="search-overlay" data-search-overlay>
  <div class="search-inner container" style="position:relative;">
    <button type="button" class="icon-btn search-close" data-search-close aria-label="Close search">''' + ICONS["CLOSE_ICON"] + '''</button>
    <div class="eyebrow">Search</div>
    <div class="search-field">
      ''' + ICONS["SEARCH_ICON"] + '''
      <input type="text" data-search-input placeholder="Search “diamond”, “Azure”, “ring”…" aria-label="Search products">
    </div>
    <p class="search-hint" data-search-hint>Try a gemstone, material, collection or category — e.g. “sapphire”, “gold”, “Muse”, “bracelet”.</p>
    <div class="search-results" data-search-results></div>
  </div>
</div>

<!-- Private enquiry modal -->
<div class="modal-backdrop" data-enquiry-modal>
  <div class="modal" role="dialog" aria-modal="true" aria-labelledby="enquiryTitle">
    <button type="button" class="modal-close" data-modal-close aria-label="Close">''' + ICONS["CLOSE_ICON"] + '''</button>
    <div class="eyebrow">Private Enquiry</div>
    <h2 id="enquiryTitle">Enquire for this piece</h2>
    <p class="modal-sub">Share your details and a member of CHICC Client Service will contact you personally.</p>
    <form novalidate>
      <div class="form-row">
        <label for="enq-piece">Piece</label>
        <input type="text" id="enq-piece" name="piece" data-piece-field readonly>
      </div>
      <div class="form-grid">
        <div class="form-row">
          <label for="enq-name">Full Name</label>
          <input type="text" id="enq-name" name="fullName" required autocomplete="name">
        </div>
        <div class="form-row">
          <label for="enq-email">Email Address</label>
          <input type="email" id="enq-email" name="email" required autocomplete="email">
        </div>
      </div>
      <div class="form-grid">
        <div class="form-row">
          <label for="enq-phone">Phone Number</label>
          <input type="tel" id="enq-phone" name="phone" autocomplete="tel">
        </div>
        <div class="form-row">
          <label for="enq-country">Country</label>
          <input type="text" id="enq-country" name="country" autocomplete="country-name">
        </div>
      </div>
      <div class="form-row">
        <label for="enq-message">Message</label>
        <textarea id="enq-message" name="message" placeholder="Tell us about sizing, customisation or anything else we can help with."></textarea>
      </div>
      <button type="submit" class="btn btn-gold btn-block">Send Enquiry</button>
    </form>
    <div class="form-success" data-form-success style="display:none;">
      <div class="tick">&#10003;</div>
      <h3>Thank you.</h3>
      <p>CHICC Client Service will contact you shortly.</p>
    </div>
  </div>
</div>

<!-- Private appointment modal -->
<div class="modal-backdrop" data-appointment-modal>
  <div class="modal" role="dialog" aria-modal="true" aria-labelledby="apptTitle">
    <button type="button" class="modal-close" data-modal-close aria-label="Close">''' + ICONS["CLOSE_ICON"] + '''</button>
    <div class="eyebrow">Client Service</div>
    <h2 id="apptTitle">Book a Private Appointment</h2>
    <p class="modal-sub">Visit our atelier for a one-to-one consultation with a CHICC jewellery specialist.</p>
    <form novalidate>
      <div class="form-grid">
        <div class="form-row">
          <label for="appt-name">Name</label>
          <input type="text" id="appt-name" name="fullName" required autocomplete="name">
        </div>
        <div class="form-row">
          <label for="appt-email">Email</label>
          <input type="email" id="appt-email" name="email" required autocomplete="email">
        </div>
      </div>
      <div class="form-grid">
        <div class="form-row">
          <label for="appt-phone">Phone</label>
          <input type="tel" id="appt-phone" name="phone" autocomplete="tel">
        </div>
        <div class="form-row">
          <label for="appt-country">Country</label>
          <input type="text" id="appt-country" name="country" autocomplete="country-name">
        </div>
      </div>
      <div class="form-grid">
        <div class="form-row">
          <label for="appt-date">Preferred Date</label>
          <input type="date" id="appt-date" name="preferredDate">
        </div>
        <div class="form-row">
          <label for="appt-time">Preferred Time</label>
          <input type="time" id="appt-time" name="preferredTime">
        </div>
      </div>
      <div class="form-grid">
        <div class="form-row">
          <label for="appt-location">Preferred Location</label>
          <select id="appt-location" name="location">
            <option>Paris Atelier</option>
            <option>London Salon</option>
            <option>New York Salon</option>
            <option>Virtual Appointment</option>
          </select>
        </div>
        <div class="form-row">
          <label for="appt-piece">Interested Piece</label>
          <input type="text" id="appt-piece" name="piece" data-piece-field placeholder="Optional">
        </div>
      </div>
      <div class="form-row">
        <label for="appt-message">Message</label>
        <textarea id="appt-message" name="message" placeholder="Anything you'd like us to prepare for your visit."></textarea>
      </div>
      <button type="submit" class="btn btn-gold btn-block">Request Appointment</button>
    </form>
    <div class="form-success" data-form-success style="display:none;">
      <div class="tick">&#10003;</div>
      <h3>Thank you.</h3>
      <p>CHICC Client Service will confirm your appointment shortly.</p>
    </div>
  </div>
</div>
'''

def scripts(extra=""):
    return f'''<script src="products.js"></script>
<script src="script.js"></script>
{extra}</body>
</html>
'''

# ----------------------------------------------------------------------
# HOMEPAGE
# ----------------------------------------------------------------------
homepage = head(
    "Home",
    "CHICC is a modern European fine jewellery maison. Timeless design, exceptional craftsmanship, jewellery to be lived in and passed on.",
    full_title="CHICC Jewellery — Made To Be Remembered",
) + HEADER + '''
<main id="main">
  <section class="hero">
    <div class="hero-slides">
      <div class="hero-slide is-active"><img src="assets/hero/hero-1.svg" alt="CHICC fine jewellery editorial composition featuring a diamond solitaire ring" width="1800" height="1250"></div>
      <div class="hero-slide"><img src="assets/hero/hero-2.svg" alt="CHICC fine jewellery editorial composition in warm gold tones" width="1800" height="1250"></div>
      <div class="hero-slide"><img src="assets/hero/hero-3.svg" alt="CHICC fine jewellery editorial composition in rose gold tones" width="1800" height="1250"></div>
    </div>
    <div class="hero-content">
      <div class="eyebrow">Fine Jewellery</div>
      <h1>Made to be<br>remembered.</h1>
      <p class="lede">Timeless design. Exceptional craftsmanship. Jewellery to be lived in and passed on.</p>
      <a href="rings.html" class="btn btn-gold">Explore Collections</a>
    </div>
    <div class="hero-controls">
      <div class="hero-arrows">
        <button type="button" class="hero-arrow" data-hero-prev aria-label="Previous slide">&#8592;</button>
        <button type="button" class="hero-arrow" data-hero-next aria-label="Next slide">&#8594;</button>
      </div>
      <div class="hero-indicators">
        <button type="button" data-hero-dot class="is-active">01</button>
        <button type="button" data-hero-dot>02</button>
        <button type="button" data-hero-dot>03</button>
      </div>
    </div>
  </section>

  <section class="benefits container">
    <div class="benefit">
      <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M12 2 3 7v6c0 5 4 8 9 9 5-1 9-4 9-9V7l-9-5Z"/><path d="M9 12l2 2 4-4"/></svg></div>
      <h3>Crafted to Last</h3>
      <p>Exceptional materials.<br>Timeless design.</p>
    </div>
    <div class="benefit">
      <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M12 21s-7-4.5-9.5-9C.7 8.3 2.8 4 7 4c2 0 3.7 1.1 5 3 1.3-1.9 3-3 5-3 4.2 0 6.3 4.3 4.5 8-2.5 4.5-9.5 9-9.5 9Z"/></svg></div>
      <h3>Private Appointments</h3>
      <p>Book a one-to-one consultation<br>in our atelier.</p>
    </div>
    <div class="benefit">
      <div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M3 8l9-5 9 5-9 5-9-5Z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg></div>
      <h3>Worldwide Delivery</h3>
      <p>Complimentary &amp; fully insured<br>delivery.</p>
    </div>
  </section>

  <section class="section container">
    <div class="section-head">
      <h2>Collections</h2>
      <a class="view-all" href="rings.html">View All</a>
    </div>
    <div class="collections-grid">
''' + "\n".join(f'''      <a class="collection-card" href="{['rings','necklaces','earrings','bracelets'][i%4]}.html?collection={c['id']}">
        <img src="{c['image']}" alt="CHICC {c['name']} collection — {c['tagline']}" loading="lazy" width="900" height="1100">
        <div class="cc-label"><div class="name">{c['name']}</div><div class="tag">{c['tagline']}</div></div>
      </a>''' for i, c in enumerate([
        {"id": "eclat", "name": "ÉCLAT", "tagline": "Timeless diamonds", "image": "assets/collections/eclat.svg"},
        {"id": "azure", "name": "AZURE", "tagline": "Sapphires &amp; beyond", "image": "assets/collections/azure.svg"},
        {"id": "lumiere", "name": "LUMIÈRE", "tagline": "Everyday essentials", "image": "assets/collections/lumiere.svg"},
        {"id": "muse", "name": "MUSE", "tagline": "Bold. Feminine. Iconic.", "image": "assets/collections/muse.svg"},
      ])) + '''
    </div>
  </section>

  <section class="section maison-split container">
    <div class="maison-media">
      <img src="assets/editorial/maison-1.svg" alt="Editorial CHICC maison composition" loading="lazy" width="1400" height="1700">
    </div>
    <div class="maison-copy">
      <div class="eyebrow">Maison CHICC</div>
      <h2>A house of modern heirlooms.</h2>
      <p class="lede">CHICC is more than jewellery. It is a story of craftsmanship, emotion and legacy. Each creation is designed to be cherished today, tomorrow and always.</p>
      <a href="maison.html" class="btn btn-outline">Discover Our Story</a>
    </div>
  </section>

  <section class="section container">
    <div class="section-head">
      <h2>New In</h2>
      <a class="view-all" href="rings.html">View All</a>
    </div>
    <div class="product-grid" data-new-in-grid></div>
  </section>
</main>
''' + FOOTER + MODALS + scripts()

W("index.html", homepage)

# ----------------------------------------------------------------------
# CATEGORY PAGES
# ----------------------------------------------------------------------
CATEGORY_META = {
    "rings": dict(title="Rings", lede="Symbols of love, strength and timeless elegance.",
                  desc="Diamond, sapphire, emerald and ruby rings in white, yellow and rose gold — crafted by the CHICC atelier."),
    "necklaces": dict(title="Necklaces", lede="Delicate lines designed to be worn every day, and pieces made to command a room.",
                       desc="Diamond pendants, sapphire drops, tennis necklaces and gold medallions from the CHICC maison."),
    "earrings": dict(title="Earrings", lede="From everyday diamond studs to sculptural drops for the evening.",
                      desc="Diamond, sapphire, emerald, ruby and pearl earrings in fine 18K gold and platinum."),
    "bracelets": dict(title="Bracelets", lede="Fine lines for the wrist — worn alone, or layered without limit.",
                       desc="Diamond tennis bracelets, gold chains and gemstone bangles crafted by CHICC."),
}

MATERIALS = ["White Gold", "Yellow Gold", "Rose Gold", "Platinum"]
GEMSTONES = ["Diamond", "Sapphire", "Emerald", "Ruby", "Pearl", "Onyx"]
COLLECTIONS_LIST = ["Éclat", "Azure", "Lumière", "Muse", "Nocturne", "Rosée"]

def filter_group(title, group, options):
    opts = "\n".join(
        f'''          <label class="filter-option">
            <input type="checkbox" data-filter="{group}" value="{o}">
            <span>{o}</span>
          </label>''' for o in options
    )
    return f'''        <div class="filter-group">
          <div class="fg-title">{title}</div>
{opts}
        </div>'''

def catalogue_sidebar():
    return f'''      <aside class="filter-panel" aria-label="Filters">
        <h2 class="fp-title">Filter By</h2>
{filter_group("Material", "material", MATERIALS)}
{filter_group("Gemstone", "gemstone", GEMSTONES)}
{filter_group("Collection", "collection", COLLECTIONS_LIST)}
        <button type="button" class="reset-filters" data-reset-filters disabled>Reset Filters</button>
      </aside>'''

def filter_drawer():
    return f'''<div class="filter-drawer-backdrop" data-filter-backdrop></div>
<div class="filter-drawer" data-filter-drawer aria-label="Filters">
  <div class="filter-drawer-head">
    <h2 class="fp-title" style="margin:0;">Filter By</h2>
    <button type="button" class="icon-btn" data-filter-close aria-label="Close filters">{ICONS["CLOSE_ICON"]}</button>
  </div>
{filter_group("Material", "material", MATERIALS)}
{filter_group("Gemstone", "gemstone", GEMSTONES)}
{filter_group("Collection", "collection", COLLECTIONS_LIST)}
  <div class="filter-drawer-foot">
    <button type="button" class="btn btn-outline" data-reset-filters disabled>Reset</button>
    <button type="button" class="btn btn-gold" data-filter-apply>View Results</button>
  </div>
</div>'''

for cat, meta in CATEGORY_META.items():
    page = head(meta["title"], meta["desc"], active=cat, body_attrs=f' data-category="{cat}"') + HEADER + f'''
<main id="main">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a><span class="sep">/</span><span class="current">{meta['title'].upper()}</span>
    </nav>
    <div class="category-head">
      <h1>{meta['title']}</h1>
      <p class="lede">{meta['lede']}</p>
    </div>

    <div class="catalogue">
{catalogue_sidebar()}
      <div class="catalogue-main">
        <div class="catalogue-toolbar">
          <div class="result-count" data-result-count>&nbsp;</div>
          <div style="display:flex; align-items:center; gap:16px;">
            <button type="button" class="btn btn-outline btn-sm filter-toggle-btn" data-filter-open>Filter</button>
            <div class="sort-control">
              <label for="sortSelect">Sort By</label>
              <select id="sortSelect" data-sort-select>
                <option value="featured">Featured</option>
                <option value="newest">Newest</option>
                <option value="name-asc">Name A–Z</option>
                <option value="name-desc">Name Z–A</option>
              </select>
            </div>
          </div>
        </div>
        <div class="product-grid" data-product-grid></div>
      </div>
    </div>
  </div>
</main>
{filter_drawer()}
''' + FOOTER + MODALS + scripts()
    W(f"{cat}.html", page)

# ----------------------------------------------------------------------
# PRODUCT DETAIL PAGE (data-driven — content filled in by script.js)
# ----------------------------------------------------------------------
product_page = head(
    "Product", "Discover exceptional fine jewellery from the CHICC maison.",
) + HEADER + f'''
<main id="main">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a><span class="sep">/</span>
      <a data-breadcrumb-category href="rings.html">RINGS</a><span class="sep">/</span>
      <span class="current" data-breadcrumb-product>PRODUCT</span>
    </nav>

    <div class="pdp" data-pdp-root>
      <div class="pdp-layout">
        <div class="pdp-thumbs" data-pdp-thumbs></div>
        <div class="pdp-main">
          <img data-pdp-main-img src="" alt="" width="1000" height="1250">
        </div>
        <div class="pdp-info">
          <div class="pc-collection" data-pdp-collection></div>
          <h1 data-pdp-name></h1>
          <p class="pdp-material" data-pdp-material></p>
          <p class="pdp-desc" data-pdp-desc></p>

          <div class="accordion">
            <div class="accordion-item">
              <button type="button" class="accordion-trigger" aria-expanded="false" aria-controls="accDetails">
                <span>Details</span><span class="plus">+</span>
              </button>
              <div class="accordion-panel" id="accDetails">
                <div class="inner">Each CHICC piece is hallmarked and finished by hand in our atelier. Ring sizing, engraving and bespoke adjustments are available on request through our Client Service team.</div>
              </div>
            </div>
            <div class="accordion-item">
              <button type="button" class="accordion-trigger" aria-expanded="false" aria-controls="accGem">
                <span>Gemstone</span><span class="plus">+</span>
              </button>
              <div class="accordion-panel" id="accGem">
                <div class="inner">All gemstones are ethically sourced and independently graded. Certificates of authenticity accompany every high jewellery piece and are available on request for fine jewellery.</div>
              </div>
            </div>
            <div class="accordion-item">
              <button type="button" class="accordion-trigger" aria-expanded="false" aria-controls="accCraft">
                <span>Craftsmanship</span><span class="plus">+</span>
              </button>
              <div class="accordion-panel" id="accCraft">
                <div class="inner">Designed and finished by CHICC master jewellers using traditional hand-setting techniques, refined over generations and paired with contemporary precision engineering.</div>
              </div>
            </div>
            <div class="accordion-item">
              <button type="button" class="accordion-trigger" aria-expanded="false" aria-controls="accDelivery">
                <span>Delivery &amp; Returns</span><span class="plus">+</span>
              </button>
              <div class="accordion-panel" id="accDelivery">
                <div class="inner">Complimentary, fully insured worldwide delivery. Complimentary 30-day returns on fine jewellery; high jewellery and bespoke commissions are final sale unless otherwise agreed with Client Service.</div>
              </div>
            </div>
          </div>

          <div class="pdp-ctas">
            <button type="button" class="btn btn-gold" data-pdp-enquire data-enquire-open>Enquire for Price</button>
            <button type="button" class="btn btn-outline" data-pdp-appointment data-appointment-open>Book a Private Appointment</button>
          </div>
          <div class="pdp-meta-links">
            <button type="button" data-pdp-wish data-wish-toggle="">{ICONS["HEART_ICON"]}<span>Add to Wishlist</span></button>
          </div>
        </div>
      </div>

      <section class="related container" style="padding-left:0;padding-right:0;">
        <div class="section-head">
          <h2>You May Also Like</h2>
        </div>
        <div class="product-grid" data-related-grid></div>
      </section>
    </div>
  </div>
</main>
''' + FOOTER + MODALS + scripts()
W("product.html", product_page)

# ----------------------------------------------------------------------
# WISHLIST PAGE
# ----------------------------------------------------------------------
wishlist_page = head(
    "Wishlist", "Your saved CHICC fine jewellery pieces.",
) + HEADER + '''
<main id="main">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a><span class="sep">/</span><span class="current">WISHLIST</span>
    </nav>
    <div class="category-head">
      <h1>Your Wishlist</h1>
      <p class="lede">Pieces you have saved to consider or discuss with our Client Service team.</p>
    </div>
    <div class="product-grid" data-wishlist-grid style="padding-bottom:110px;"></div>
  </div>
</main>
''' + FOOTER + MODALS + '''<script src="products.js"></script>
<script src="script.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function () {
  function render() {
    var ids = JSON.parse(localStorage.getItem("chicc_wishlist") || "[]");
    var items = CHICC_PRODUCTS.filter(function (p) { return ids.indexOf(p.id) > -1; });
    var grid = document.querySelector("[data-wishlist-grid]");
    if (!items.length) {
      grid.innerHTML = '<div class="empty-state"><p>Your wishlist is empty. Browse our collections and tap the heart icon to save pieces here.</p><a class="btn btn-outline" href="rings.html">Explore Rings</a></div>';
      return;
    }
    window.__chiccRenderWishlist ? window.__chiccRenderWishlist(grid, items) : null;
  }
  document.addEventListener("chicc:wishlist-change", render);
  setTimeout(render, 0);
});
</script>
</body>
</html>
'''
W("wishlist.html", wishlist_page)

# ----------------------------------------------------------------------
# MAISON CHICC (about) PAGE
# ----------------------------------------------------------------------
maison_page = head(
    "Maison CHICC",
    "The story of CHICC — a modern European fine jewellery maison built on craftsmanship, emotion and legacy.",
) + HEADER + '''
<main id="main">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a><span class="sep">/</span><span class="current">MAISON CHICC</span>
    </nav>
    <div class="page-header">
      <div class="eyebrow">Maison CHICC</div>
      <h1>A house of modern heirlooms.</h1>
    </div>
  </div>

  <section class="section maison-split container">
    <div class="maison-media">
      <img src="assets/editorial/maison-1.svg" alt="Editorial CHICC maison composition" loading="lazy" width="1400" height="1700">
    </div>
    <div class="maison-copy">
      <div class="eyebrow">Our Story</div>
      <h2>Founded on restraint, worn with confidence.</h2>
      <p class="lede">CHICC is more than jewellery. It is a story of craftsmanship, emotion and legacy. Each creation is designed to be cherished today, tomorrow and always.</p>
      <p class="body-text">Founded in Paris, CHICC was born from a belief that fine jewellery should feel personal rather than performative — pieces designed to be worn daily, not reserved for a single occasion. Every silhouette begins as a sketch in our atelier and passes through the hands of master jewellers before it ever reaches a client.</p>
    </div>
  </section>

  <section class="section maison-split reverse container" id="craftsmanship">
    <div class="maison-media">
      <img src="assets/editorial/maison-2.svg" alt="Editorial CHICC atelier composition" loading="lazy" width="1400" height="1700">
    </div>
    <div class="maison-copy">
      <div class="eyebrow">Expert Craftsmanship</div>
      <h2>Made by hand, made to last.</h2>
      <p class="body-text">Our master jewellers train for years before setting a single stone on a client commission. Techniques passed between generations are paired with contemporary precision engineering, so that every CHICC piece is as structurally sound as it is beautiful — designed to be worn, and passed on.</p>
    </div>
  </section>

  <section class="section container" id="high-jewellery">
    <div class="section-head">
      <h2>High Jewellery</h2>
    </div>
    <p class="lede" style="max-width:640px; margin-bottom:40px;">Beyond our fine jewellery collections, CHICC High Jewellery offers bespoke, one-of-a-kind commissions — exceptional gemstones set in sculptural, hand-finished designs created exclusively for private clients.</p>
    <div class="values-grid">
      <div class="value-card">
        <h3>Bespoke Commissions</h3>
        <p>Work directly with our design studio to create a piece unique to you, from a single sketch to the final setting.</p>
      </div>
      <div class="value-card">
        <h3>Exceptional Gemstones</h3>
        <p>Rare diamonds and coloured gemstones sourced and graded to the highest international standards.</p>
      </div>
      <div class="value-card">
        <h3>By Appointment</h3>
        <p>High Jewellery consultations take place privately in our ateliers, or wherever is most convenient for you.</p>
      </div>
    </div>
    <div style="margin-top:44px; display:flex; gap:16px; flex-wrap:wrap;">
      <button type="button" class="btn btn-gold" data-appointment-open data-piece="High Jewellery Consultation">Book a Private Appointment</button>
      <button type="button" class="btn btn-outline" data-enquire-open data-piece="High Jewellery Enquiry">Enquire</button>
    </div>
  </section>

  <section class="section container" id="sourcing">
    <div class="section-head"><h2>Our Commitments</h2></div>
    <div class="values-grid">
      <div class="value-card" id="care">
        <h3>Lifetime Care</h3>
        <p>Complimentary cleaning, polishing and structural inspection for the lifetime of every CHICC piece.</p>
      </div>
      <div class="value-card">
        <h3>Ethical &amp; Conflict-Free Sourcing</h3>
        <p>All diamonds and gemstones are sourced in accordance with the Kimberley Process and our internal responsible-sourcing standards.</p>
      </div>
      <div class="value-card">
        <h3>Private Client Service</h3>
        <p>A dedicated advisor for every client, available for sizing, customisation and ongoing care — <a class="link-underline" href="contact.html#client-services">reach our team</a>.</p>
      </div>
    </div>
  </section>
</main>
''' + FOOTER + MODALS + scripts()
W("maison.html", maison_page)

# ----------------------------------------------------------------------
# CONTACT PAGE
# ----------------------------------------------------------------------
contact_page = head(
    "Contact",
    "Contact CHICC Jewellery Client Service, or book a private appointment at one of our ateliers.",
) + HEADER + '''
<main id="main">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a><span class="sep">/</span><span class="current">CONTACT</span>
    </nav>
    <div class="page-header">
      <div class="eyebrow">Client Service</div>
      <h1>We would love to hear from you.</h1>
      <p class="lede">For pricing, availability, customisation or private appointments, our Client Service team is here to help.</p>
    </div>
  </div>

  <section class="simple-page container" id="client-services">
    <div class="two-col">
      <div>
        <h2 style="margin-bottom:24px;">Get in Touch</h2>
        <p class="body-text" style="margin-bottom:30px;">Send a general enquiry and a member of our Client Service team will respond personally, usually within one business day.</p>
        <button type="button" class="btn btn-gold" data-enquire-open data-piece="General Enquiry">Send an Enquiry</button>
      </div>
      <div class="contact-card" id="appointment">
        <div class="eyebrow">By Appointment</div>
        <h3>Book a Private Appointment</h3>
        <p>Visit our atelier in Paris, London or New York — or meet with us virtually, wherever you are.</p>
        <button type="button" class="btn btn-outline" data-appointment-open>Book Appointment</button>
      </div>
    </div>

    <div class="values-grid" style="margin-top:80px;">
      <div class="value-card">
        <h3>Paris Atelier</h3>
        <p>8 Place Vend&ocirc;me, 75001 Paris<br>By appointment, Mon&ndash;Sat</p>
      </div>
      <div class="value-card">
        <h3>London Salon</h3>
        <p>172 New Bond Street, London W1S<br>By appointment, Mon&ndash;Sat</p>
      </div>
      <div class="value-card">
        <h3>New York Salon</h3>
        <p>745 Fifth Avenue, New York, NY<br>By appointment, Mon&ndash;Sat</p>
      </div>
    </div>

    <div class="values-grid" style="margin-top:40px;">
      <div class="value-card">
        <h3>Client Service</h3>
        <p>+33 1 42 00 00 00<br>hello@chicc-jewellery.com</p>
      </div>
      <div class="value-card">
        <h3>Lifetime Care</h3>
        <p>Complimentary cleaning, polishing and inspection for every CHICC piece — <a class="link-underline" href="maison.html#care">learn more</a>.</p>
      </div>
      <div class="value-card">
        <h3>High Jewellery</h3>
        <p>Bespoke commissions and bridal consultations — <a class="link-underline" href="maison.html#high-jewellery">discover High Jewellery</a>.</p>
      </div>
    </div>
  </section>
</main>
''' + FOOTER + MODALS + scripts()
W("contact.html", contact_page)

print("HTML pages generated.")
