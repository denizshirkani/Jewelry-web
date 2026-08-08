/* ==========================================================================
   CHICC JEWELLERY — site interactivity
   Requires products.js (CHICC_PRODUCTS, CHICC_COLLECTIONS) loaded first.
   ========================================================================== */
(function () {
  "use strict";

  /* ------------------------------------------------------------------ */
  /*  Path helpers — keep the site working from any nesting level        */
  /* ------------------------------------------------------------------ */
  const ROOT = (function () {
    // All pages live at repository root, so a plain relative path works
    // both locally, on GitHub Pages project sites and on Vercel.
    return "";
  })();

  function productUrl(p) {
    return `product.html?id=${encodeURIComponent(p.id)}`;
  }

  function byId(id) {
    return CHICC_PRODUCTS.find((p) => p.id === id);
  }

  /* ------------------------------------------------------------------ */
  /*  Icons (inline, no external requests)                               */
  /* ------------------------------------------------------------------ */
  const ICONS = {
    heart: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 20.5s-7.5-4.6-10-9.4C.5 7.4 2.6 4 6.3 4c2 0 3.6 1 5.7 3.2C14.1 5 15.7 4 17.7 4c3.7 0 5.8 3.4 4.3 7.1-2.5 4.8-10 9.4-10 9.4Z"/></svg>',
    heartFill: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 20.5s-7.5-4.6-10-9.4C.5 7.4 2.6 4 6.3 4c2 0 3.6 1 5.7 3.2C14.1 5 15.7 4 17.7 4c3.7 0 5.8 3.4 4.3 7.1-2.5 4.8-10 9.4-10 9.4Z"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="11" cy="11" r="7.2"/><path d="M21 21l-4.4-4.4"/></svg>',
    user: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="8" r="3.6"/><path d="M4.5 20c1.6-3.6 4.6-5.4 7.5-5.4s5.9 1.8 7.5 5.4"/></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M5 5l14 14M19 5L5 19"/></svg>',
    arrowLeft: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M18 12H6M11 6l-6 6 6 6"/></svg>',
    arrowRight: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M6 12h12M13 6l6 6-6 6"/></svg>',
  };

  /* ------------------------------------------------------------------ */
  /*  Wishlist (localStorage)                                            */
  /* ------------------------------------------------------------------ */
  const WISHLIST_KEY = "chicc_wishlist";

  function getWishlist() {
    try {
      return JSON.parse(localStorage.getItem(WISHLIST_KEY)) || [];
    } catch (e) {
      return [];
    }
  }

  function setWishlist(ids) {
    localStorage.setItem(WISHLIST_KEY, JSON.stringify(ids));
    updateWishlistCount();
    document.dispatchEvent(new CustomEvent("chicc:wishlist-change", { detail: ids }));
  }

  function isWishlisted(id) {
    return getWishlist().includes(id);
  }

  function toggleWishlist(id) {
    const list = getWishlist();
    const idx = list.indexOf(id);
    if (idx > -1) {
      list.splice(idx, 1);
    } else {
      list.push(id);
    }
    setWishlist(list);
    return list.includes(id);
  }

  function updateWishlistCount() {
    const count = getWishlist().length;
    document.querySelectorAll("[data-wishlist-count]").forEach((el) => {
      el.textContent = count > 0 ? String(count) : "";
      el.style.display = count > 0 ? "flex" : "none";
    });
  }

  function refreshWishlistButtons(root = document) {
    root.querySelectorAll("[data-wish-toggle]").forEach((btn) => {
      const id = btn.getAttribute("data-wish-toggle");
      const active = isWishlisted(id);
      btn.classList.toggle("is-active", active);
      btn.innerHTML = active ? ICONS.heartFill : ICONS.heart;
      btn.setAttribute("aria-pressed", active ? "true" : "false");
      btn.setAttribute("aria-label", active ? "Remove from wishlist" : "Add to wishlist");
    });
  }

  function bindWishlistButtons(root = document) {
    root.querySelectorAll("[data-wish-toggle]").forEach((btn) => {
      if (btn.__wishBound) return;
      btn.__wishBound = true;
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        const id = btn.getAttribute("data-wish-toggle");
        const nowActive = toggleWishlist(id);
        refreshWishlistButtons(document);
        showToast(nowActive ? "Added to your wishlist" : "Removed from your wishlist");
      });
    });
  }

  document.addEventListener("chicc:wishlist-change", () => refreshWishlistButtons(document));

  /* ------------------------------------------------------------------ */
  /*  Toast                                                               */
  /* ------------------------------------------------------------------ */
  let toastTimer = null;
  function showToast(msg) {
    let toast = document.querySelector(".toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "toast";
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 2600);
  }

  /* ------------------------------------------------------------------ */
  /*  Product card markup (shared by home / category / search / related) */
  /* ------------------------------------------------------------------ */
  function productCardHTML(p) {
    const img = p.images && p.images[0] ? p.images[0] : "";
    const imgAlt = `${p.name} — ${p.material}${p.gemstone.length ? ", " + p.gemstone.join(" & ") : ""}, CHICC ${p.collection} collection`;
    return `
      <article class="product-card" data-id="${p.id}" data-material="${p.material}" data-gemstone="${p.gemstone.join(",")}" data-collection="${p.collection}" data-new="${p.new}" data-featured="${p.featured}" data-sort="${p.sortOrder}" data-name="${p.name.replace(/"/g, "&quot;")}">
        <a class="pc-media" href="${productUrl(p)}" aria-label="View ${p.name}">
          ${p.new ? '<span class="new-badge">New</span>' : ""}
          <img src="${img}" alt="${imgAlt}" loading="lazy" width="800" height="1000">
        </a>
        <button type="button" class="pc-wish" data-wish-toggle="${p.id}" aria-label="Add to wishlist" aria-pressed="false">${ICONS.heart}</button>
        <div class="pc-body">
          <div class="pc-collection">${p.collection}</div>
          <h3 class="pc-name"><a href="${productUrl(p)}">${p.name}</a></h3>
          <div class="pc-material">18K ${p.material}${p.gemstone.length ? " · " + p.gemstone.join(" & ") : ""}</div>
          <div class="pc-actions">
            <button type="button" class="btn btn-outline btn-sm" data-enquire-open data-piece="${p.name.replace(/"/g, "&quot;")}" data-piece-id="${p.id}">Enquire</button>
          </div>
        </div>
      </article>`;
  }

  function renderGrid(container, products) {
    if (!container) return;
    if (!products.length) {
      container.innerHTML = `<div class="empty-state"><p>No pieces match your current selection.</p></div>`;
      return;
    }
    container.innerHTML = products.map(productCardHTML).join("");
    bindWishlistButtons(container);
    refreshWishlistButtons(container);
    bindEnquireButtons(container);
  }

  /* ------------------------------------------------------------------ */
  /*  Header: sticky shrink + mobile menu                                 */
  /* ------------------------------------------------------------------ */
  function initHeader() {
    const header = document.querySelector(".site-header");
    if (header) {
      const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 30);
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }

    const burger = document.querySelector("[data-menu-open]");
    const menu = document.querySelector(".mobile-menu");
    const menuClose = document.querySelector("[data-menu-close]");
    function openMenu() {
      menu.classList.add("is-open");
      document.body.style.overflow = "hidden";
      burger.setAttribute("aria-expanded", "true");
    }
    function closeMenu() {
      menu.classList.remove("is-open");
      document.body.style.overflow = "";
      burger.setAttribute("aria-expanded", "false");
    }
    if (burger && menu) {
      burger.addEventListener("click", openMenu);
      menuClose && menuClose.addEventListener("click", closeMenu);
      menu.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeMenu));
      window.__chiccCloseMenu = closeMenu;
    }
  }

  /* ------------------------------------------------------------------ */
  /*  Hero carousel                                                       */
  /* ------------------------------------------------------------------ */
  function initHero() {
    const hero = document.querySelector(".hero");
    if (!hero) return;
    const slides = Array.from(hero.querySelectorAll(".hero-slide"));
    const dots = Array.from(hero.querySelectorAll("[data-hero-dot]"));
    let idx = 0;
    let timer;

    function go(n) {
      idx = (n + slides.length) % slides.length;
      slides.forEach((s, i) => s.classList.toggle("is-active", i === idx));
      dots.forEach((d, i) => d.classList.toggle("is-active", i === idx));
    }
    function next() { go(idx + 1); }
    function prev() { go(idx - 1); }
    function restart() {
      clearInterval(timer);
      timer = setInterval(next, 6500);
    }

    hero.querySelector("[data-hero-next]")?.addEventListener("click", () => { next(); restart(); });
    hero.querySelector("[data-hero-prev]")?.addEventListener("click", () => { prev(); restart(); });
    dots.forEach((d, i) => d.addEventListener("click", () => { go(i); restart(); }));

    if (slides.length > 1) restart();
  }

  /* ------------------------------------------------------------------ */
  /*  Homepage: New In                                                    */
  /* ------------------------------------------------------------------ */
  function initNewIn() {
    const grid = document.querySelector("[data-new-in-grid]");
    if (!grid) return;
    const items = CHICC_PRODUCTS.filter((p) => p.new).sort((a, b) => a.sortOrder - b.sortOrder).slice(0, 4);
    renderGrid(grid, items);
  }

  /* ------------------------------------------------------------------ */
  /*  Category (catalogue) pages                                         */
  /* ------------------------------------------------------------------ */
  const COLLECTION_ID_TO_NAME = { eclat: "Éclat", azure: "Azure", lumiere: "Lumière", muse: "Muse", nocturne: "Nocturne", rosee: "Rosée" };

  function initCategoryPage(category) {
    const grid = document.querySelector("[data-product-grid]");
    if (!grid) return;
    const all = CHICC_PRODUCTS.filter((p) => p.category === category);

    const state = { material: new Set(), gemstone: new Set(), collection: new Set(), sort: "featured" };

    // Deep-link support, e.g. rings.html?collection=eclat from homepage cards
    const urlParams = new URLSearchParams(window.location.search);
    const collectionParam = urlParams.get("collection");
    if (collectionParam && COLLECTION_ID_TO_NAME[collectionParam]) {
      state.collection.add(COLLECTION_ID_TO_NAME[collectionParam]);
    }

    const countEl = document.querySelector("[data-result-count]");
    const sortSelect = document.querySelector("[data-sort-select]");
    const resetBtn = document.querySelector("[data-reset-filters]");
    const checkboxes = Array.from(document.querySelectorAll("[data-filter]"));

    function apply() {
      let list = all.filter((p) => {
        if (state.material.size && !state.material.has(p.material)) return false;
        if (state.gemstone.size && !p.gemstone.some((g) => state.gemstone.has(g))) return false;
        if (state.collection.size && !state.collection.has(p.collection)) return false;
        return true;
      });
      switch (state.sort) {
        case "newest":
          list = list.slice().sort((a, b) => (b.new === a.new ? a.sortOrder - b.sortOrder : b.new ? 1 : -1));
          break;
        case "name-asc":
          list = list.slice().sort((a, b) => a.name.localeCompare(b.name));
          break;
        case "name-desc":
          list = list.slice().sort((a, b) => b.name.localeCompare(a.name));
          break;
        default:
          list = list.slice().sort((a, b) => (b.featured === a.featured ? a.sortOrder - b.sortOrder : b.featured ? 1 : -1));
      }
      renderGrid(grid, list);
      if (countEl) countEl.textContent = `${list.length} piece${list.length === 1 ? "" : "s"}`;
      const anyActive = state.material.size || state.gemstone.size || state.collection.size;
      if (resetBtn) resetBtn.disabled = !anyActive;
    }

    checkboxes.forEach((cb) => {
      const group = cb.getAttribute("data-filter");
      if (state[group] && state[group].has(cb.value)) cb.checked = true;
    });

    checkboxes.forEach((cb) => {
      cb.addEventListener("change", () => {
        const group = cb.getAttribute("data-filter");
        const val = cb.value;
        state[group][cb.checked ? "add" : "delete"](val);
        apply();
      });
    });

    sortSelect && sortSelect.addEventListener("change", () => {
      state.sort = sortSelect.value;
      apply();
    });

    resetBtn && resetBtn.addEventListener("click", () => {
      state.material.clear();
      state.gemstone.clear();
      state.collection.clear();
      state.sort = "featured";
      checkboxes.forEach((cb) => (cb.checked = false));
      if (sortSelect) sortSelect.value = "featured";
      apply();
    });

    // mobile filter drawer
    const drawer = document.querySelector("[data-filter-drawer]");
    const backdrop = document.querySelector("[data-filter-backdrop]");
    const openBtn = document.querySelector("[data-filter-open]");
    const closeBtn = document.querySelector("[data-filter-close]");
    const applyBtn = document.querySelector("[data-filter-apply]");
    function openDrawer() {
      drawer?.classList.add("is-open");
      backdrop?.classList.add("is-open");
      document.body.style.overflow = "hidden";
    }
    function closeDrawer() {
      drawer?.classList.remove("is-open");
      backdrop?.classList.remove("is-open");
      document.body.style.overflow = "";
    }
    openBtn && openBtn.addEventListener("click", openDrawer);
    closeBtn && closeBtn.addEventListener("click", closeDrawer);
    backdrop && backdrop.addEventListener("click", closeDrawer);
    applyBtn && applyBtn.addEventListener("click", closeDrawer);
    window.__chiccCloseDrawer = closeDrawer;

    apply();
  }

  /* ------------------------------------------------------------------ */
  /*  Accordions                                                          */
  /* ------------------------------------------------------------------ */
  function initAccordions(root = document) {
    root.querySelectorAll(".accordion-trigger").forEach((btn) => {
      if (btn.__accBound) return;
      btn.__accBound = true;
      btn.addEventListener("click", () => {
        const expanded = btn.getAttribute("aria-expanded") === "true";
        const panel = document.getElementById(btn.getAttribute("aria-controls"));
        btn.setAttribute("aria-expanded", String(!expanded));
        if (panel) {
          panel.style.maxHeight = expanded ? "0px" : panel.scrollHeight + "px";
        }
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /*  Product detail page                                                 */
  /* ------------------------------------------------------------------ */
  function initProductDetail() {
    const root = document.querySelector("[data-pdp-root]");
    if (!root) return;
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");
    const product = byId(id) || CHICC_PRODUCTS[0];

    document.title = `${product.name} — CHICC Jewellery`;

    document.querySelector("[data-pdp-collection]").textContent = product.collection;
    document.querySelector("[data-pdp-name]").textContent = product.name;
    document.querySelector("[data-pdp-material]").textContent = `18K ${product.material}${product.gemstone.length ? " · " + product.gemstone.join(" & ") : ""}`;
    document.querySelector("[data-pdp-desc]").textContent = product.description;
    document.querySelector("[data-breadcrumb-category]").textContent = capitalize(product.category);
    document.querySelector("[data-breadcrumb-category]").setAttribute("href", `${product.category}.html`);
    document.querySelector("[data-breadcrumb-product]").textContent = product.name.toUpperCase();

    const mainImg = document.querySelector("[data-pdp-main-img]");
    const thumbWrap = document.querySelector("[data-pdp-thumbs]");
    thumbWrap.innerHTML = product.images.map((src, i) => `
      <button type="button" class="${i === 0 ? "is-active" : ""}" data-thumb-idx="${i}" aria-label="View image ${i + 1}">
        <img src="${src}" alt="${product.name} view ${i + 1}" loading="lazy">
      </button>`).join("");
    mainImg.src = product.images[0];
    mainImg.alt = `${product.name}, ${product.material}${product.gemstone.length ? " with " + product.gemstone.join(" & ") : ""}`;

    thumbWrap.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        thumbWrap.querySelectorAll("button").forEach((b) => b.classList.remove("is-active"));
        btn.classList.add("is-active");
        const i = Number(btn.getAttribute("data-thumb-idx"));
        mainImg.style.opacity = "0";
        setTimeout(() => {
          mainImg.src = product.images[i];
          mainImg.style.opacity = "1";
        }, 120);
      });
    });

    // wishlist + enquire wiring
    const wishBtn = document.querySelector("[data-pdp-wish]");
    if (wishBtn) {
      wishBtn.setAttribute("data-wish-toggle", product.id);
      bindWishlistButtons(document);
      refreshWishlistButtons(document);
    }
    const enquireBtn = document.querySelector("[data-pdp-enquire]");
    if (enquireBtn) {
      enquireBtn.setAttribute("data-piece", product.name);
      enquireBtn.setAttribute("data-piece-id", product.id);
    }
    const apptBtn = document.querySelector("[data-pdp-appointment]");
    if (apptBtn) {
      apptBtn.setAttribute("data-piece", product.name);
    }
    bindEnquireButtons(document);
    bindAppointmentButtons(document);
    initAccordions(document);

    // related products: same collection first, fallback same category
    const related = CHICC_PRODUCTS.filter((p) => p.id !== product.id && p.collection === product.collection)
      .concat(CHICC_PRODUCTS.filter((p) => p.id !== product.id && p.category === product.category && p.collection !== product.collection))
      .slice(0, 3);
    const relatedGrid = document.querySelector("[data-related-grid]");
    if (relatedGrid) renderGrid(relatedGrid, related);
  }

  function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  /* ------------------------------------------------------------------ */
  /*  Enquiry modal                                                       */
  /* ------------------------------------------------------------------ */
  function bindEnquireButtons(root = document) {
    root.querySelectorAll("[data-enquire-open]").forEach((btn) => {
      if (btn.__enqBound) return;
      btn.__enqBound = true;
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        const piece = btn.getAttribute("data-piece") || "";
        openEnquiryModal(piece);
      });
    });
  }

  function openEnquiryModal(piece) {
    const modal = document.querySelector("[data-enquiry-modal]");
    if (!modal) return;
    const form = modal.querySelector("form");
    const successEl = modal.querySelector("[data-form-success]");
    form.style.display = "";
    successEl.style.display = "none";
    form.reset();
    const pieceField = modal.querySelector("[data-piece-field]");
    if (pieceField) pieceField.value = piece || "General enquiry";
    openModal(modal);
  }

  function bindAppointmentButtons(root = document) {
    root.querySelectorAll("[data-appointment-open]").forEach((btn) => {
      if (btn.__apptBound) return;
      btn.__apptBound = true;
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const piece = btn.getAttribute("data-piece") || "";
        const modal = document.querySelector("[data-appointment-modal]");
        if (!modal) return;
        const form = modal.querySelector("form");
        const successEl = modal.querySelector("[data-form-success]");
        form.style.display = "";
        successEl.style.display = "none";
        form.reset();
        const pieceField = modal.querySelector("[data-piece-field]");
        if (pieceField && piece) pieceField.value = piece;
        openModal(modal);
      });
    });
  }

  function openModal(modal) {
    modal.classList.add("is-open");
    document.body.style.overflow = "hidden";
    const focusable = modal.querySelector("input, textarea, select, button");
    focusable && focusable.focus({ preventScroll: true });
  }
  function closeModal(modal) {
    modal.classList.remove("is-open");
    document.body.style.overflow = "";
  }

  function initModals() {
    document.querySelectorAll(".modal-backdrop").forEach((modal) => {
      modal.querySelectorAll("[data-modal-close]").forEach((btn) => btn.addEventListener("click", () => closeModal(modal)));
      modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal(modal);
      });
      const form = modal.querySelector("form");
      if (form) {
        form.addEventListener("submit", (e) => {
          e.preventDefault();
          // Front-end confirmation only. Structured for a future backend:
          // POST to /api/enquiry or an email provider (e.g. Formspree/Resend)
          // using the same field names present in this form.
          const data = Object.fromEntries(new FormData(form).entries());
          console.info("[CHICC] form submission (front-end only)", data);
          form.style.display = "none";
          const successEl = modal.querySelector("[data-form-success]");
          if (successEl) successEl.style.display = "block";
        });
      }
    });
    window.__chiccCloseAllModals = () => {
      document.querySelectorAll(".modal-backdrop.is-open").forEach(closeModal);
    };
  }

  /* ------------------------------------------------------------------ */
  /*  Search overlay                                                      */
  /* ------------------------------------------------------------------ */
  function initSearch() {
    const overlay = document.querySelector("[data-search-overlay]");
    const openBtns = document.querySelectorAll("[data-search-open]");
    const closeBtn = document.querySelector("[data-search-close]");
    const input = document.querySelector("[data-search-input]");
    const results = document.querySelector("[data-search-results]");
    const hint = document.querySelector("[data-search-hint]");
    if (!overlay) return;

    function open() {
      overlay.classList.add("is-open");
      document.body.style.overflow = "hidden";
      setTimeout(() => input && input.focus(), 200);
    }
    function close() {
      overlay.classList.remove("is-open");
      document.body.style.overflow = "";
    }
    openBtns.forEach((b) => b.addEventListener("click", open));
    closeBtn && closeBtn.addEventListener("click", close);
    window.__chiccCloseSearch = close;

    function runSearch(q) {
      q = q.trim().toLowerCase();
      if (!q) {
        results.innerHTML = "";
        hint.style.display = "block";
        return;
      }
      hint.style.display = "none";
      const matches = CHICC_PRODUCTS.filter((p) => {
        const hay = [p.name, p.category, p.collection, p.material, ...p.gemstone].join(" ").toLowerCase();
        return hay.includes(q);
      }).slice(0, 9);
      if (!matches.length) {
        results.innerHTML = `<div class="search-empty">No pieces found for “${escapeHtml(q)}”. Try “diamond”, “sapphire” or a collection name.</div>`;
        results.style.display = "block";
        results.style.gridTemplateColumns = "1fr";
        return;
      }
      results.style.display = "grid";
      results.style.gridTemplateColumns = "";
      results.innerHTML = matches.map(productCardHTML).join("");
      bindWishlistButtons(results);
      refreshWishlistButtons(results);
      bindEnquireButtons(results);
    }

    input && input.addEventListener("input", () => runSearch(input.value));
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  /* ------------------------------------------------------------------ */
  /*  Escape key: close whatever is open                                  */
  /* ------------------------------------------------------------------ */
  function initEscapeHandling() {
    document.addEventListener("keydown", (e) => {
      if (e.key !== "Escape") return;
      window.__chiccCloseAllModals && window.__chiccCloseAllModals();
      window.__chiccCloseSearch && window.__chiccCloseSearch();
      window.__chiccCloseMenu && window.__chiccCloseMenu();
      window.__chiccCloseDrawer && window.__chiccCloseDrawer();
    });
  }

  /* ------------------------------------------------------------------ */
  /*  Init                                                                */
  /* ------------------------------------------------------------------ */
  window.__chiccRenderWishlist = renderGrid;

  document.addEventListener("DOMContentLoaded", () => {
    updateWishlistCount();
    initHeader();
    initHero();
    initModals();
    initSearch();
    initEscapeHandling();
    initNewIn();
    initAccordions(document);
    bindEnquireButtons(document);
    bindAppointmentButtons(document);

    const category = document.body.getAttribute("data-category");
    if (category) initCategoryPage(category);

    initProductDetail();

    bindWishlistButtons(document);
    refreshWishlistButtons(document);
  });
})();
