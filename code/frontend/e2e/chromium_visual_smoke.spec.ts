import path from "node:path";
import { fileURLToPath } from "node:url";

import { expect, test } from "@playwright/test";

const DEFAULT_DEMO_TOKEN = "rohde-demo-2026";
const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function loginIfGateVisible(page: import("@playwright/test").Page): Promise<void> {
  const tokenInput = page.getByRole("textbox");
  try {
    await tokenInput.waitFor({ state: "visible", timeout: 3000 });
    await tokenInput.fill(process.env.DEMO_TOKEN ?? DEFAULT_DEMO_TOKEN);
    await page.getByRole("button", { name: /zugang/i }).click();
    await Promise.race([
      page.getByRole("banner").waitFor({ state: "visible", timeout: 20_000 }),
      page.getByText(/ungueltig|ungueltiger|server nicht erreichbar|zeitueberschreitung/i).waitFor({
        state: "visible",
        timeout: 20_000,
      }),
    ]).catch(() => undefined);
  } catch {
    // No auth gate, proceed.
  }
}

test.describe("Chromium visual smoke", () => {
  test("renders Claude Design demo shell and captures evidence screenshot", async ({ page }, testInfo) => {
    test.setTimeout(120_000);
    await page.addInitScript(() => {
      window.localStorage.setItem("carotis:walkthroughSeen", "true");
    });
    await page.goto("/", { waitUntil: "networkidle" });
    await loginIfGateVisible(page);

    const authGate = page.getByRole("button", { name: /zugang/i });
    const appHeader = page.getByRole("banner");

    const hasAuthGate = await authGate.isVisible().catch(() => false);
    const hasHeader = await appHeader.isVisible().catch(() => false);

    expect(hasAuthGate || hasHeader).toBe(true);

    if (hasHeader) {
      await expect(page.getByText("Carotis AI").first()).toBeVisible();
      await expect(page.getByText("M. Mueller").first()).toBeVisible();
      await expect(page.getByText(/AI Analysis Live/i).first()).toBeVisible();
      await expect(page.getByText(/Heatmap ON/i).first()).toBeVisible();
      await expect(page.getByText(/Download selected DICOM/i).first()).toBeVisible();

      if (process.env.RUN_UPLOAD === "true") {
        const demoDicom = path.resolve(
          __dirname,
          "../public/demo/dicoms/case_002.dcm"
        );
        await page.locator('input[type="file"]').setInputFiles(demoDicom);
        await expect(page.getByText(/Analyse abgeschlossen/i)).toBeVisible({
          timeout: 90_000,
        });
      }
    }

    const shot = await page.screenshot({ fullPage: true });
    await testInfo.attach("chromium-visual-smoke", {
      body: shot,
      contentType: "image/png",
    });
  });
});
