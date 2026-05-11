import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { AuthGate } from "./AuthGate";

// Mock store
vi.mock("@/store", () => ({
  useStore: () => ({ setPhysicianRoleHash: vi.fn() }),
}));

// Mock i18n
vi.mock("@/lib/i18n", () => ({
  t: (key: string) => key,
}));

describe("AuthGate", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it("renders login form when no token", () => {
    render(<AuthGate>protected</AuthGate>);
    expect(screen.getByLabelText(/Demo-Token/i)).toBeInTheDocument();
  });

  it("input is type=password for shoulder-surfing protection", () => {
    render(<AuthGate>protected</AuthGate>);
    const input = screen.getByLabelText(/Demo-Token/i);
    expect(input).toHaveAttribute("type", "password");
  });

  it("shows timeout error when fetch aborts", async () => {
    global.fetch = vi.fn(() => new Promise<Response>((_, reject) => {
      setTimeout(() => {
        const err = new Error("The operation was aborted");
        err.name = "AbortError";
        reject(err);
      }, 10);
    }));

    render(<AuthGate>protected</AuthGate>);
    const input = screen.getByLabelText(/Demo-Token/i);
    fireEvent.change(input, { target: { value: "test-token-123" } });
    fireEvent.click(screen.getByRole("button", { name: /Zugang freischalten/i }));

    await waitFor(() => {
      expect(screen.getByText(/Zeit/i)).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it("shows server unreachable error on network failure", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("Network error"));

    render(<AuthGate>protected</AuthGate>);
    const input = screen.getByLabelText(/Demo-Token/i);
    fireEvent.change(input, { target: { value: "test-token-123" } });
    fireEvent.click(screen.getByRole("button", { name: /Zugang freischalten/i }));

    await waitFor(() => {
      expect(screen.getByText(/Server nicht erreichbar/i)).toBeInTheDocument();
    });
  });
});
