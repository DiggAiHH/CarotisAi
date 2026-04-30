export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export class UnauthorizedError extends ApiError {
  constructor(message = "Unauthorized") {
    super(message, 401, "UNAUTHORIZED");
    this.name = "UnauthorizedError";
  }
}

export class RateLimitError extends ApiError {
  public retryAfter: number;
  constructor(message = "Rate limit exceeded", retryAfter = 60) {
    super(message, 429, "RATE_LIMITED");
    this.name = "RateLimitError";
    this.retryAfter = retryAfter;
  }
}

export class ModelNotLoadedError extends ApiError {
  constructor(message = "Model not loaded") {
    super(message, 503, "MODEL_NOT_LOADED");
    this.name = "ModelNotLoadedError";
  }
}

export class ValidationError extends ApiError {
  constructor(message = "Validation failed") {
    super(message, 422, "VALIDATION_ERROR");
    this.name = "ValidationError";
  }
}

export function isApiError(err: unknown): err is ApiError {
  return err instanceof ApiError;
}
