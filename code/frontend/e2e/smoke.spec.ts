import { expect, test } from "@playwright/test";

const DEMO_TOKEN = "rohde-demo-2026";

async function gateLogin(page: import("@playwright/test").Page) {
  const input = page.getByRole("textbox");
  try {
    await input.waitFor({ state: "visible", timeout: 3000 });
    await input.fill(DEMO_TOKEN);
    await page.getByRole("button", { name: /zugang/i }).click();
  } catch {
    // No auth gate or already logged in.
  }
}

test.describe("Smoke – Desktop", () => {
  test("renders header and 3-column layout", async ({ page }) => {
    await page.goto("/");
    await gateLogin(page);
    await expect(page.getByRole("banner")).toBeVisible();
    await expect(page.getByText(/carotis/i).first()).toBeVisible();
    // Desktop: both sidebars must be present in DOM
    await expect(page.locator("[data-walkthrough='dicom-viewer']")).toBeVisible();
    await expect(page.locator("[data-walkthrough='ai-panel']")).toBeVisible();
  });
});

test.describe("Smoke – Mobile (Pixel 5)", () => {
  test.use({ viewport: { width: 393, height: 851 } });

  test("shows bottom tab bar and viewer tab by default", async ({ page }) => {
    await page.goto("/");
    await gateLogin(page);
    await expect(page.getByRole("navigation")).toBeVisible();
    // Viewer tab is active by default — dicom area must be visible
    await expect(page.locator("[data-walkthrough='dicom-viewer']")).toBeVisible();
    // AI panel must be hidden on mobile until tab selected
    await expect(page.locator("[data-walkthrough='ai-panel']")).toBeHidden();
  });

  test("switches to AI panel via tab", async ({ page }) => {
    await page.goto("/");
    await gateLogin(page);
    await page.getByRole("button", { name: "KI" }).click();
    await expect(page.locator("[data-walkthrough='ai-panel']")).toBeVisible();
    await expect(page.locator("[data-walkthrough='dicom-viewer']")).toBeHidden();
  });
});
