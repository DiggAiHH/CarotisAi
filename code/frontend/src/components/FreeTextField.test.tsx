import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { FreeTextField } from "./FreeTextField";

type CallbackFn = (...args: unknown[]) => unknown;
type DebouncedFn = CallbackFn & { flush: () => void; cancel: () => void };

// Mock debounce to execute immediately but with stable references
const debounceCache = new Map<number, { fn: CallbackFn; wrapper: DebouncedFn }>();
vi.mock("use-debounce", () => ({
  useDebouncedCallback: (fn: CallbackFn, delay: number) => {
    if (!debounceCache.has(delay)) {
      const wrapper = ((...args: unknown[]) => debounceCache.get(delay)!.fn(...args)) as DebouncedFn;
      wrapper.flush = () => {};
      wrapper.cancel = () => {};
      debounceCache.set(delay, { fn, wrapper });
      return wrapper;
    }
    debounceCache.get(delay)!.fn = fn;
    return debounceCache.get(delay)!.wrapper;
  },
}));

// Mock apiClient
const mockCheckText = vi.fn();
vi.mock("@/lib/apiClient", () => ({
  apiClient: {
    checkText: (...args: unknown[]) => mockCheckText(...args),
  },
}));

describe("FreeTextField", () => {
  beforeEach(() => {
    mockCheckText.mockReset();
    localStorage.clear();
  });

  it("renders textarea with correct aria attributes when clean", () => {
    mockCheckText.mockResolvedValue({ is_clean: true, pii_spans: [] });
    render(<FreeTextField value="" onChange={vi.fn()} />);
    const ta = screen.getByRole("textbox");
    expect(ta).toHaveAttribute("aria-invalid", "false");
  });

  it("renders textarea with aria-invalid=true when PII detected", async () => {
    mockCheckText.mockResolvedValue({
      is_clean: false,
      pii_spans: [{ start: 0, end: 5, label: "PATIENT_NAME" }],
    });
    render(<FreeTextField value="Hans Mueller" onChange={vi.fn()} />);
    await waitFor(() => {
      const ta = screen.getByRole("textbox");
      expect(ta).toHaveAttribute("aria-invalid", "true");
      expect(ta).toHaveAttribute("aria-describedby", "pii-warning");
    });
  });

  it("shows alert role on PII warning", async () => {
    mockCheckText.mockResolvedValue({
      is_clean: false,
      pii_spans: [{ start: 0, end: 5, label: "PATIENT_NAME" }],
    });
    render(<FreeTextField value="Hans Mueller" onChange={vi.fn()} />);
    await waitFor(() => {
      const warning = screen.getByRole("alert");
      expect(warning).toBeInTheDocument();
    });
  });

  it("calls onPIIStatusChange when PII found", async () => {
    const onPII = vi.fn();
    mockCheckText.mockResolvedValue({
      is_clean: false,
      pii_spans: [{ start: 0, end: 5, label: "PATIENT_NAME" }],
    });
    render(<FreeTextField value="Hans Mueller" onChange={vi.fn()} onPIIStatusChange={onPII} />);
    await waitFor(() => {
      expect(onPII).toHaveBeenCalledWith(true);
    });
  });

  it("calls onPIIStatusChange(false) when text is clean", async () => {
    const onPII = vi.fn();
    mockCheckText.mockResolvedValue({ is_clean: true, pii_spans: [] });
    render(<FreeTextField value="Clean text" onChange={vi.fn()} onPIIStatusChange={onPII} />);
    await waitFor(() => {
      expect(onPII).toHaveBeenCalledWith(false);
    });
  });

  it("respects maxLength", () => {
    const onChange = vi.fn();
    render(<FreeTextField value="" onChange={onChange} maxLength={10} />);
    const ta = screen.getByRole("textbox");
    fireEvent.change(ta, { target: { value: "a".repeat(20) } });
    expect(onChange).toHaveBeenCalledWith("a".repeat(10));
  });
});
