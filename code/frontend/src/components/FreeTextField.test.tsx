import { describe, expect, it, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { FreeTextField } from "./FreeTextField";

describe("FreeTextField", () => {
  it("renders textarea with placeholder", () => {
    render(<FreeTextField value="" onChange={() => {}} />);
    expect(
      screen.getByPlaceholderText(/Plaque-Form unklar/)
    ).toBeInTheDocument();
  });

  it("calls onChange when typing", () => {
    const handleChange = vi.fn();
    render(<FreeTextField value="" onChange={handleChange} />);
    const textarea = screen.getByRole("textbox");
    fireEvent.change(textarea, { target: { value: "test note" } });
    expect(handleChange).toHaveBeenCalledWith("test note");
  });

  it("respects maxLength", () => {
    const handleChange = vi.fn();
    render(<FreeTextField value="abc" onChange={handleChange} maxLength={5} />);
    const textarea = screen.getByRole("textbox");
    fireEvent.change(textarea, { target: { value: "abcdefgh" } });
    expect(handleChange).toHaveBeenCalledWith("abcde");
  });
});
