import { chromium } from 'playwright';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(here, 'og-preview.html');
const outputPath = path.join(here, '..', 'assets', 'og', 'og-preview-v2.jpg');

const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' });
  await page.evaluate(async () => { await document.fonts.ready; });

  const loaded = await page.evaluate(() => document.fonts.check('600 72px "Golos Text"'));
  if (!loaded) {
    throw new Error('Golos Text did not load; refusing to build fallback-font OG preview');
  }

  const computed = await page.locator('h1').evaluate((el) => {
    const s = getComputedStyle(el);
    return { family: s.fontFamily, weight: s.fontWeight, spacing: s.letterSpacing, lineHeight: s.lineHeight };
  });
  console.log('OG heading typography:', computed);

  await page.screenshot({ path: outputPath, type: 'jpeg', quality: 94, fullPage: false });
  console.log(`Built ${outputPath} at 1200x630 with browser-rendered Golos Text`);
} finally {
  await browser.close();
}
