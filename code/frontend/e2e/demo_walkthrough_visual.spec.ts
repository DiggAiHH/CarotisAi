import { expect, test } from "@playwright/test";

const DEMO_TOKEN = process.env.DEMO_TOKEN ?? "rohde-demo-2026";

async function gateLogin(page: import("@playwright/test").Page) {
  const input = page.getByRole("textbox");
  try {
    await input.waitFor({ state: "visible", timeout: 3000 });
    await input.fill(DEMO_TOKEN);
    await page.getByRole("button", { name: /zugang/i }).click();
    await page.waitForLoadState("networkidle");
  } catch {
    // No auth gate or already logged in
  }
}

async function attachScreenshot(
  page: import("@playwright/test").Page,
  testInfo: import("@playwright/test").TestInfo,
  name: string,
) {
  const shot = await page.screenshot({ fullPage: true });
  await testInfo.attach(name, { body: shot, contentType: "image/png" });
}

test.describe("Demo Walkthrough — Desktop", () => {
  test("full patient-to-ai journey with evidence screenshots", async ({ page }, testInfo) => {
    // Step 1: Token Gate
    await page.goto("/", { waitUntil: "networkidle" });
    await attachScreenshot(page, testInfo, "01-token-gate");

    // Step 2: Login
    await gateLogin(page);
    await expect(page.getByRole("banner")).toBeVisible();
    await attachScreenshot(page, testInfo, "02-app-loaded");

    // Step 3: Patients list visible
    await expect(page.getByText(/Müller|Schmidt|Weber|Fischer/i).first()).toBeVisible();
    await attachScreenshot(page, testInfo, "03-patients-list");

    // Step 4: Select first patient
    const firstPatient = page.getByRole("button").filter({ hasText: /\d+%/ }).first();
    if (await firstPatient.isVisible().catch(() => false)) {
      await firstPatient.click();
      await page.waitForTimeout(300);
      await attachScreenshot(page, testInfo, "04-patient-selected");
    }

    // Step 5: DICOM Viewer visible
    await expect(page.locator("[data-walkthrough='dicom-viewer']")).toBeVisible();
    await attachScreenshot(page, testInfo, "05-dicom-viewer");

    // Step 6: AI Panel visible
    await expect(page.locator("[data-walkthrough='ai-panel']")).toBeVisible();
    await attachScreenshot(page, testInfo, "06-ai-panel");

    // Step 7: Confidence badge visible
    const confidenceBadge = page.getByText(/%/).first();
    await expect(confidenceBadge).toBeVisible();
    await attachScreenshot(page, testInfo, "07-confidence-badge");
  });
});

test.describe("Demo Walkthrough — Mobile", () => {
  test.use({ viewport: { width: 393, height: 851 } });

  test("tab navigation with evidence screenshots", async ({ page }, testInfo) => {
    await page.goto("/", { waitUntil: "networkidle" });
    await gateLogin(page);

    // Step 1: Mobile app shell
    await expect(page.getByRole("banner")).toBeVisible();
    await expect(page.getByRole("navigation")).toBeVisible();
    await attachScreenshot(page, testInfo, "m01-mobile-shell");

    // Step 2: Viewer tab (default)
    await expect(page.locator("[data-walkthrough='dicom-viewer']")).toBeVisible();
    await attachScreenshot(page, testInfo, "m02-mobile-viewer");

    // Step 3: Switch to AI tab
    await page.getByRole("button", { name: "KI" }).click();
    await expect(page.locator("[data-walkthrough='ai-panel']")).toBeVisible();
    await attachScreenshot(page, testInfo, "m03-mobile-ai");

    // Step 4: Switch to Patients tab
    await page.getByRole("button", { name: /Patienten|Liste/i }).click();
    await expect(page.getByText(/Müller|Schmidt|Weber|Fischer/i).first()).toBeVisible();
    await attachScreenshot(page, testInfo, "m04-mobile-patients");
  });
});
