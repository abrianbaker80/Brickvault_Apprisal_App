import { mkdir } from 'node:fs/promises';
import { chromium, expect } from '@playwright/test';

const baseURL = process.env.BVA_E2E_API_URL;
if (!/^http:\/\/127\.0\.0\.1:[0-9]+$/u.test(baseURL ?? ''))
  throw Error('Owned loopback TEST API required');
const root = process.env.BVA_OUTCOME_ROOT;
const child = process.env.BVA_OUTCOME_CHILD;
const output = '.local/phase16a-chatgpt';
await mkdir(output, { recursive: true });
const browser = await chromium.launch();
try {
  const context = await browser.newContext({
    baseURL,
    viewport: { width: 1440, height: 1000 },
    serviceWorkers: 'block',
  });
  const page = await context.newPage();
  const errors = [];
  const forbidden = [];
  const outcomeWrites = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await context.route('**/*', (route) => {
    const request = route.request();
    const url = new URL(request.url());
    if (url.origin !== baseURL || /market-refresh|product-refresh/u.test(url.pathname)) {
      forbidden.push(`${request.method()} ${url.origin}${url.pathname}`);
      return route.abort();
    }
    if (request.method() === 'POST' && url.pathname.endsWith('/outcome'))
      outcomeWrites.push(url.pathname);
    return route.continue();
  });
  const clock = new Date(process.env.BVA_TEST_TIME);
  const day = (offset) => new Date(clock.getTime() + offset * 86400000).toISOString().slice(0, 10);
  await page.clock.install({ time: clock });
  await page.goto(`/deals/${child}`);
  await page.getByLabel('Password', { exact: true }).fill(process.env.BVA_E2E_PASSWORD);
  await page.getByRole('button', { name: 'Sign in', exact: true }).click();
  const section = page.getByRole('region', { name: 'Actual outcome', exact: true });
  await expect(section.getByRole('button', { name: 'Record outcome', exact: true })).toBeVisible();
  await section.getByRole('button', { name: 'Record outcome', exact: true }).click();
  await section.getByLabel('Acquisition date', { exact: true }).fill(day(1));
  await section.getByLabel('Inspected contents', { exact: true }).selectOption('CONFIRMED_MATCH');
  await section.getByLabel('Inspection date', { exact: true }).fill(day(1));
  await section
    .getByLabel('Original forecast preceded purchase', { exact: true })
    .selectOption('true');
  await section.getByLabel('Own labor minutes', { exact: true }).fill('60');
  await section.getByLabel('Sale status', { exact: true }).selectOption('COMPLETE');
  await section.getByLabel('Sale strategy', { exact: true }).selectOption('COMPLETE_SET');
  await section.getByLabel('Sale condition', { exact: true }).selectOption('N');
  await section.getByLabel('Sale channel', { exact: true }).fill('Synthetic sale');
  await section.getByLabel('Final sale date', { exact: true }).fill(day(11));
  for (const [label, value] of [
    ['Actual purchase price', '100'],
    ['Actual acquisition extras', '5'],
    ['Replacement costs', '3'],
    ['Paid labor costs', '7'],
    ['Item sale proceeds', '180'],
    ['Shipping received from buyer', '12'],
    ['Selling fees', '18'],
    ['Shipping paid', '10'],
    ['Other selling costs', '2'],
  ])
    await section.getByLabel(`${label} (USD)`, { exact: true }).fill(value);
  expect(outcomeWrites).toHaveLength(0);
  const firstResponse = page.waitForResponse(
    (response) => response.request().method() === 'POST' && response.url().endsWith('/outcome'),
  );
  await section.getByRole('button', { name: 'Save outcome', exact: true }).click();
  const first = await firstResponse;
  expect(first.status()).toBe(200);
  const firstBody = await first.json();
  expect(firstBody.results.profit.amount).toBe('47.00');
  expect(firstBody.results.days_to_sell).toBe(10);
  expect(first.headers()['cache-control']).toBe('no-store');
  await expect(
    section.getByText('Outcome revision 1 saved. Original forecast unchanged.', { exact: true }),
  ).toBeVisible();
  await section.screenshot({ path: `${output}/outcome-desktop.png` });

  await page.setViewportSize({ width: 320, height: 1000 });
  await section.getByRole('button', { name: 'Correct entry', exact: true }).click();
  await section.getByLabel('Actual purchase price (USD)', { exact: true }).fill('90');
  await section
    .getByLabel('Correction reason', { exact: true })
    .fill('Receipt corrected acquisition price');
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(320);
  await section.screenshot({ path: `${output}/outcome-correction-320.png` });
  const correctionResponse = page.waitForResponse(
    (response) => response.request().method() === 'POST' && response.url().endsWith('/outcome'),
  );
  await section.getByRole('button', { name: 'Save correction', exact: true }).click();
  const second = await correctionResponse;
  expect(second.status()).toBe(200);
  const secondBody = await second.json();
  expect(secondBody.revision).toBe(2);
  expect(secondBody.results.profit.amount).toBe('57.00');
  expect(secondBody.root_forecast_id).toBe(root);
  await page.goto(`/deals/${root}`);
  await expect(
    section.getByRole('heading', { name: 'Recorded outcome · revision 2' }),
  ).toBeVisible();
  await section.getByText('Outcome history', { selector: 'summary', exact: true }).click();
  await section.getByRole('button', { name: 'View outcome revision 1', exact: true }).click();
  const old = section.getByRole('region', { name: 'Historical actual outcome', exact: true });
  await expect(old.getByText('$47.00 USD', { exact: true })).toBeVisible();
  await expect(
    section
      .getByRole('region', { name: 'Recorded actual outcome', exact: true })
      .getByText('$57.00 USD', { exact: true }),
  ).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(320);
  await section.screenshot({ path: `${output}/outcome-history-320.png` });
  expect(outcomeWrites).toHaveLength(2);
  expect(errors).toEqual([]);
  expect(forbidden).toEqual([]);
  expect(
    await page.evaluate(() => ({ local: localStorage.length, session: sessionStorage.length })),
  ).toEqual({ local: 0, session: 0 });
  console.log(
    JSON.stringify({
      outcome_revisions: 2,
      original_id: root,
      child_id: child,
      history_preserved: true,
      desktop_and_320px: true,
      original_actual_profit: '47.00',
      corrected_actual_profit: '57.00',
      explicit_outcome_writes: outcomeWrites.length,
      errors,
      forbidden,
      persistent_private_browser_storage: false,
      screenshots: [
        'outcome-desktop.png',
        'outcome-correction-320.png',
        'outcome-history-320.png',
      ].map((name) => `${output}/${name}`),
      evidence:
        'One real synthetic outcome/correction/history flow; owned TEST PostgreSQL/API and Chromium',
    }),
  );
} finally {
  await browser.close();
}
