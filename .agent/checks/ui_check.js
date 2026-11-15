// UI check: start the server, open the page in headless Chromium, click Start on a fast and a
// detailed method, hover a selector segment, save screenshots here, and count console errors.
// Run from the repo root:  NODE_PATH=$(npm root -g) node .agent/checks/ui_check.js
const { spawn } = require("child_process");
const path = require("path");
const { chromium } = require("playwright");

const OUT = __dirname;
const ROOT = path.resolve(__dirname, "..", "..");

function startServer() {
  return new Promise((resolve, reject) => {
    const proc = spawn("python", ["-m", "aerosim", "serve", "--port", "0"], { cwd: ROOT });
    proc.stdout.on("data", buf => {
      const m = String(buf).match(/http:\/\/localhost:(\d+)/);
      if (m) resolve({ proc, url: `http://localhost:${m[1]}/` });
    });
    proc.stderr.on("data", buf => process.stderr.write(buf));
    proc.on("exit", code => reject(new Error(`server exited with ${code}`)));
  });
}

async function runRow(page, row, methodIndex) {
  const r = page.locator(`.row[data-row="${row}"]`);
  if (!(await r.getAttribute("class")).includes("open")) await r.locator(".row-head").click();
  await r.locator(".capsule button").nth(methodIndex).click();
  await r.locator(".start").click();
  await page.waitForFunction(sel => !document.querySelector(sel).disabled,
    `.row[data-row="${row}"] .start`, { timeout: 120000 });
  return (await r.locator(".result").textContent()).trim();
}

(async () => {
  const { proc, url } = await startServer();
  const errors = [];
  const browser = await chromium.launch({ args: ["--use-gl=swiftshader", "--enable-unsafe-swiftshader"] });
  try {
    const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
    page.on("console", msg => { if (msg.type() === "error") errors.push(msg.text()); });
    page.on("pageerror", err => errors.push(String(err)));
    await page.goto(url);
    await page.waitForSelector(".row .capsule button");
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(OUT, "ui_1_start.png") });

    console.log("fast   solid/Formula     :", await runRow(page, "solid", 0));
    await page.locator('.row[data-row="solid"] .capsule button').nth(1).hover();
    await page.waitForTimeout(300);
    console.log("tooltip:", (await page.locator("#tip").textContent()).slice(0, 90), "…");
    await page.screenshot({ path: path.join(OUT, "ui_2_hover.png") });

    console.log("detailed solid/Pixel FV  :", await runRow(page, "solid", 1));
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(OUT, "ui_3_pixel_fv.png") });

    console.log("detailed structure/defects:", await runRow(page, "structure", 1));
    console.log("detailed solid/Pixel FV  :", await runRow(page, "solid", 1));
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(OUT, "ui_4_defects.png") });
    console.log("footer:", (await page.locator("footer").innerText()).replace(/\n/g, " | "));
  } finally {
    await browser.close();
    proc.kill();
  }
  console.log(`console errors: ${errors.length}`);
  errors.forEach(e => console.log("  " + e));
  process.exit(errors.length ? 1 : 0);
})().catch(err => { console.error(err); process.exit(1); });
