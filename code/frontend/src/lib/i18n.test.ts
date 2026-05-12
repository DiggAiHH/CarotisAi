import { describe, expect, it, vi } from "vitest";
import { t } from "./i18n";

describe("i18n", () => {
  it("returns the German string for a known key", () => {
    expect(t("app.title")).toBe("Carotis-AI");
    expect(t("app.online")).toBe("Online");
    expect(t("status.done")).toBe("Analyse abgeschlossen");
  });

  it("substitutes variables with {key} pattern", () => {
    expect(t("tour.progress", { current: "2", total: "5" })).toBe(
      "Schritt 2 von 5",
    );
    expect(t("tour.progress", { current: "1", total: "3" })).toBe(
      "Schritt 1 von 3",
    );
  });

  it("falls back to the raw key and warns when key is missing", () => {
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});
    const missingKey = "this.key.does.not.exist";

    expect(t(missingKey)).toBe(missingKey);
    expect(warnSpy).toHaveBeenCalledWith("missing-i18n-key", missingKey);

    warnSpy.mockRestore();
  });
});
