const { chromium } = require('playwright');
const BASE = 'http://localhost:8123';

const pages = ['index.html', 'rings.html', 'necklaces.html', 'earrings.html', 'bracelets.html', 'maison.html', 'contact.html', 'wishlist.html'];

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let failures = [];

  // ---- 1. Console errors + broken network requests across every page ----
  for (const p of pages) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const consoleErrors = [];
    const badRequests = [];
    page.on('console', (msg) => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
    page.on('response', (res) => {
      if (res.status() >= 400) badRequests.push(`${res.status()} ${res.url()}`);
    });
    page.on('pageerror', (err) => consoleErrors.push('pageerror: ' + err.message));
    await page.goto(`${BASE}/${p}`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(300);
    if (consoleErrors.length) failures.push(`[${p}] console errors: ${JSON.stringify(consoleErrors)}`);
    if (badRequests.length) failures.push(`[${p}] bad requests: ${JSON.stringify(badRequests)}`);

    // check every <img> actually has natural size > 0 (not broken/black)
    const brokenImgs = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('img')).filter(img => img.complete && img.naturalWidth === 0).map(img => img.src);
    });
    if (brokenImgs.length) failures.push(`[${p}] broken images: ${JSON.stringify(brokenImgs)}`);

    await page.close();
  }
  console.log('✓ Step 1 (console/network/images) done. Failures so far:', failures.length);

  // ---- 2. Product detail pages: sample several ids ----
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const ids = ['r001', 'n002', 'e005', 'b009'];
    for (const id of ids) {
      const errs = [];
      page.removeAllListeners('console');
      page.on('console', (msg) => { if (msg.type() === 'error') errs.push(msg.text()); });
      await page.goto(`${BASE}/product.html?id=${id}`, { waitUntil: 'networkidle' });
      const name = await page.textContent('[data-pdp-name]');
      if (!name || !name.trim()) failures.push(`[product ${id}] name not populated`);
      const mainSrc = await page.getAttribute('[data-pdp-main-img]', 'src');
      if (!mainSrc) failures.push(`[product ${id}] main image missing`);
      if (errs.length) failures.push(`[product ${id}] console errors: ${JSON.stringify(errs)}`);
    }
    await page.close();
  }
  console.log('✓ Step 2 (PDP data binding) done. Failures so far:', failures.length);

  // ---- 3. Accordion functionality + button-size-stability bug check ----
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/product.html?id=r001`, { waitUntil: 'networkidle' });
    const enquireBefore = await page.locator('[data-pdp-enquire]').boundingBox();
    const apptBefore = await page.locator('[data-pdp-appointment]').boundingBox();

    const trigger = page.locator('.accordion-trigger').first();
    await trigger.click();
    const expanded = await trigger.getAttribute('aria-expanded');
    if (expanded !== 'true') failures.push('[accordion] did not expand on click');
    const panel = page.locator('#accDetails');
    const maxH = await panel.evaluate(el => el.style.maxHeight);
    if (maxH === '0px' || maxH === '') failures.push('[accordion] panel did not open (maxHeight not set)');

    const enquireAfter = await page.locator('[data-pdp-enquire]').boundingBox();
    const apptAfter = await page.locator('[data-pdp-appointment]').boundingBox();
    if (Math.round(enquireBefore.height) !== Math.round(enquireAfter.height) || Math.round(enquireBefore.width) !== Math.round(enquireAfter.width)) {
      failures.push(`[button-stability] Enquire button resized after accordion open: ${JSON.stringify(enquireBefore)} -> ${JSON.stringify(enquireAfter)}`);
    }
    if (Math.round(apptBefore.height) !== Math.round(apptAfter.height)) {
      failures.push(`[button-stability] Appointment button resized after accordion open`);
    }

    // collapse again
    await trigger.click();
    const expanded2 = await trigger.getAttribute('aria-expanded');
    if (expanded2 !== 'false') failures.push('[accordion] did not collapse on second click');

    // second accordion independent
    const trigger2 = page.locator('.accordion-trigger').nth(1);
    await trigger2.click();
    const exp2 = await trigger2.getAttribute('aria-expanded');
    if (exp2 !== 'true') failures.push('[accordion] second accordion did not expand independently');
    const exp1AfterOther = await trigger.getAttribute('aria-expanded');
    if (exp1AfterOther !== 'false') failures.push('[accordion] opening second accordion affected first');

    await page.close();
  }
  console.log('✓ Step 3 (accordion + button stability) done. Failures so far:', failures.length);

  // ---- 4. Enquiry modal: opens, auto-populates piece, submits, shows confirmation; other buttons unaffected ----
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/product.html?id=n003`, { waitUntil: 'networkidle' });
    const wishBefore = await page.locator('[data-pdp-wish]').boundingBox();

    await page.click('[data-pdp-enquire]');
    await page.waitForTimeout(400);
    const modalOpen = await page.locator('[data-enquiry-modal]').evaluate(el => el.classList.contains('is-open'));
    if (!modalOpen) failures.push('[enquiry modal] did not open');
    const pieceVal = await page.locator('[data-enquiry-modal] [data-piece-field]').inputValue();
    if (!pieceVal.includes('Emerald')) failures.push(`[enquiry modal] piece not auto-populated correctly, got "${pieceVal}"`);

    await page.fill('[data-enquiry-modal] #enq-name', 'Jane Doe');
    await page.fill('[data-enquiry-modal] #enq-email', 'jane@example.com');
    await page.click('[data-enquiry-modal] button[type="submit"]');
    await page.waitForTimeout(300);
    const successVisible = await page.locator('[data-enquiry-modal] [data-form-success]').isVisible();
    if (!successVisible) failures.push('[enquiry modal] success message not shown after submit');

    // Escape closes it
    await page.keyboard.press('Escape');
    await page.waitForTimeout(400);
    const stillOpen = await page.locator('[data-enquiry-modal]').evaluate(el => el.classList.contains('is-open'));
    if (stillOpen) failures.push('[enquiry modal] Escape key did not close modal');

    const wishAfter = await page.locator('[data-pdp-wish]').boundingBox();
    if (Math.round(wishBefore.width) !== Math.round(wishAfter.width)) failures.push('[button-stability] wishlist button resized after modal interaction');

    await page.close();
  }
  console.log('✓ Step 4 (enquiry modal) done. Failures so far:', failures.length);

  // ---- 5. Appointment modal ----
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/contact.html`, { waitUntil: 'networkidle' });
    await page.click('[data-appointment-open]');
    await page.waitForTimeout(400);
    const open = await page.locator('[data-appointment-modal]').evaluate(el => el.classList.contains('is-open'));
    if (!open) failures.push('[appointment modal] did not open from contact page');
    await page.fill('#appt-name', 'Jane Doe');
    await page.fill('#appt-email', 'jane@example.com');
    await page.click('[data-appointment-modal] button[type="submit"]');
    await page.waitForTimeout(300);
    const ok = await page.locator('[data-appointment-modal] [data-form-success]').isVisible();
    if (!ok) failures.push('[appointment modal] success not shown');
    await page.close();
  }
  console.log('✓ Step 5 (appointment modal) done. Failures so far:', failures.length);

  // ---- 6. Wishlist: toggle, persists across reload, header count updates ----
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/rings.html`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(200);
    const firstWish = page.locator('[data-wish-toggle]').first();
    const idAttr = await firstWish.getAttribute('data-wish-toggle');
    await firstWish.click();
    await page.waitForTimeout(150);
    const activeNow = await firstWish.evaluate(el => el.classList.contains('is-active'));
    if (!activeNow) failures.push('[wishlist] heart did not activate on click');
    const countText = await page.locator('[data-wishlist-count]').first().textContent();
    if (countText.trim() !== '1') failures.push(`[wishlist] header count expected "1", got "${countText}"`);

    await page.reload({ waitUntil: 'networkidle' });
    await page.waitForTimeout(200);
    const stillActive = await page.locator(`[data-wish-toggle="${idAttr}"]`).first().evaluate(el => el.classList.contains('is-active'));
    if (!stillActive) failures.push('[wishlist] state did not persist across reload');

    await page.goto(`${BASE}/wishlist.html`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(200);
    const wishlistCards = await page.locator('[data-wishlist-grid] .product-card').count();
    if (wishlistCards !== 1) failures.push(`[wishlist page] expected 1 saved card, found ${wishlistCards}`);

    await page.close();
  }
  console.log('✓ Step 6 (wishlist persistence) done. Failures so far:', failures.length);

  // ---- 7. Filters + sort on category page ----
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/rings.html`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(200);
    const totalBefore = await page.locator('[data-product-grid] .product-card').count();
    if (totalBefore !== 9) failures.push(`[rings] expected 9 products, found ${totalBefore}`);

    await page.check('input[data-filter="gemstone"][value="Diamond"]');
    await page.waitForTimeout(150);
    const diamondCount = await page.locator('[data-product-grid] .product-card').count();
    const expectedDiamond = await page.evaluate(() => CHICC_PRODUCTS.filter(p => p.category === 'rings' && p.gemstone.includes('Diamond')).length);
    if (diamondCount !== expectedDiamond) failures.push(`[filters] Diamond filter: expected ${expectedDiamond}, got ${diamondCount}`);
    const nonDiamond = await page.locator('[data-product-grid] .product-card[data-gemstone=""]').count();

    await page.check('input[data-filter="material"][value="White Gold"]');
    await page.waitForTimeout(150);
    const combo = await page.locator('[data-product-grid] .product-card').count();
    const expectedCombo = await page.evaluate(() => CHICC_PRODUCTS.filter(p => p.category === 'rings' && p.gemstone.includes('Diamond') && p.material === 'White Gold').length);
    if (combo !== expectedCombo) failures.push(`[filters] combined filter: expected ${expectedCombo}, got ${combo}`);

    const resetBtn = page.locator('[data-reset-filters]').first();
    const disabledBeforeReset = await resetBtn.isDisabled();
    if (disabledBeforeReset) failures.push('[filters] reset button should be enabled when filters active');
    await resetBtn.click();
    await page.waitForTimeout(150);
    const afterReset = await page.locator('[data-product-grid] .product-card').count();
    if (afterReset !== 9) failures.push(`[filters] reset did not restore full set, got ${afterReset}`);
    const diamondChecked = await page.isChecked('input[data-filter="gemstone"][value="Diamond"]');
    if (diamondChecked) failures.push('[filters] checkbox not visually unchecked after reset');

    // sort
    await page.selectOption('[data-sort-select]', 'name-asc');
    await page.waitForTimeout(150);
    const names = await page.locator('[data-product-grid] .product-card [data-name]').evaluateAll(els => els.map(e => e.getAttribute('data-name')));
    const sorted = [...names].sort((a, b) => a.localeCompare(b));
    if (JSON.stringify(names) !== JSON.stringify(sorted)) failures.push(`[sort] name-asc not sorted correctly: ${JSON.stringify(names)}`);

    await page.close();
  }
  console.log('✓ Step 7 (filters + sort) done. Failures so far:', failures.length);

  // ---- 8. Category pages contain correct, non-duplicated products ----
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const catCounts = {};
    for (const cat of ['rings', 'necklaces', 'earrings', 'bracelets']) {
      await page.goto(`${BASE}/${cat}.html`, { waitUntil: 'networkidle' });
      await page.waitForTimeout(200);
      const ids = await page.locator('[data-product-grid] .product-card').evaluateAll(els => els.map(e => e.getAttribute('data-id')));
      catCounts[cat] = ids;
      const wrongCat = ids.filter(id => !id.startsWith(cat[0]));
      if (wrongCat.length) failures.push(`[category ${cat}] contains ids from another category: ${JSON.stringify(wrongCat)}`);
    }
    const allIds = Object.values(catCounts).flat();
    const dupes = allIds.filter((id, i) => allIds.indexOf(id) !== i);
    if (dupes.length) failures.push(`[category] duplicate product ids across categories: ${JSON.stringify(dupes)}`);
    await page.close();
  }
  console.log('✓ Step 8 (category correctness) done. Failures so far:', failures.length);

  // ---- 9. Search overlay ----
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/index.html`, { waitUntil: 'networkidle' });
    await page.click('[data-search-open]');
    await page.waitForTimeout(400);
    const openState = await page.locator('[data-search-overlay]').evaluate(el => el.classList.contains('is-open'));
    if (!openState) failures.push('[search] overlay did not open');
    await page.fill('[data-search-input]', 'emerald');
    await page.waitForTimeout(200);
    const results = await page.locator('[data-search-results] .product-card').count();
    const expected = await page.evaluate(() => CHICC_PRODUCTS.filter(p => (p.name + p.category + p.collection + p.material + p.gemstone.join(' ')).toLowerCase().includes('emerald')).length);
    if (results !== expected) failures.push(`[search] "emerald" expected ${expected} results, got ${results}`);

    await page.fill('[data-search-input]', 'zzz-no-match');
    await page.waitForTimeout(200);
    const emptyShown = await page.locator('.search-empty').isVisible();
    if (!emptyShown) failures.push('[search] empty state not shown for no matches');

    await page.keyboard.press('Escape');
    await page.waitForTimeout(400);
    const closedState = await page.locator('[data-search-overlay]').evaluate(el => el.classList.contains('is-open'));
    if (closedState) failures.push('[search] Escape did not close overlay');
    await page.close();
  }
  console.log('✓ Step 9 (search) done. Failures so far:', failures.length);

  // ---- 10. Mobile menu + responsive screenshots ----
  const breakpoints = [
    ['1440px', 1440, 900], ['1280px', 1280, 900], ['1024px', 1024, 900],
    ['768px', 768, 1024], ['430px', 430, 900], ['390px', 390, 900],
  ];
  for (const [label, w, h] of breakpoints) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto(`${BASE}/rings.html`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(200);
    const hasHScroll = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 2);
    if (hasHScroll) failures.push(`[responsive ${label}] horizontal scroll detected on rings.html`);
    await page.screenshot({ path: `qa_shots/rings_${label}.png`, fullPage: false });

    if (w <= 1024) {
      const burger = page.locator('[data-menu-open]');
      if (await burger.isVisible()) {
        await burger.click();
        await page.waitForTimeout(400);
        const menuOpen = await page.locator('.mobile-menu').evaluate(el => el.classList.contains('is-open'));
        if (!menuOpen) failures.push(`[responsive ${label}] mobile menu did not open`);
        await page.screenshot({ path: `qa_shots/menu_${label}.png` });
        await page.keyboard.press('Escape');
        await page.waitForTimeout(400);
        const menuClosed = await page.locator('.mobile-menu').evaluate(el => !el.classList.contains('is-open'));
        if (!menuClosed) failures.push(`[responsive ${label}] Escape did not close mobile menu`);

        const filterBtn = page.locator('[data-filter-open]');
        if (await filterBtn.isVisible()) {
          await filterBtn.click();
          await page.waitForTimeout(400);
          const drawerOpen = await page.locator('[data-filter-drawer]').evaluate(el => el.classList.contains('is-open'));
          if (!drawerOpen) failures.push(`[responsive ${label}] filter drawer did not open`);
        }
      }
    }
    await page.close();
  }
  console.log('✓ Step 10 (responsive) done. Failures so far:', failures.length);

  await browser.close();

  console.log('\n========== QA REPORT ==========');
  if (failures.length === 0) {
    console.log('ALL CHECKS PASSED ✓');
  } else {
    failures.forEach(f => console.log('FAIL: ' + f));
    console.log(`\n${failures.length} failure(s) found.`);
  }
  process.exit(failures.length ? 1 : 0);
})();
