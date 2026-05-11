type SeedRandomOptions = { global?: boolean };

function makeRandom(seed: string): () => number {
  let state = 2166136261;
  for (let i = 0; i < seed.length; i += 1) {
    state ^= seed.charCodeAt(i);
    state = Math.imul(state, 16777619);
  }
  return () => {
    state += 0x6d2b79f5;
    let value = state;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

export default function seedrandom(
  seed = "carotis",
  options: SeedRandomOptions = {}
): () => number {
  const random = makeRandom(String(seed));
  if (options.global) {
    Math.random = random;
  }
  return random;
}
