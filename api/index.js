// Vercel serverless adapter for the Tavo POS evaluation lab.
// The upstream app expects a long-running Express process and a writable local JSON file.
// For this public lab we use /tmp, which is writable per serverless instance.
if (!process.env.JWT_SECRET) process.env.JWT_SECRET = 'altamis-public-lab-only-vercel-secret-2026';
if (!process.env.DATA_DIR) process.env.DATA_DIR = '/tmp/tavo-pos-data';
if (!process.env.AUTO_SEED) process.env.AUTO_SEED = 'true';

let loaded;
async function loadApp() {
  if (!loaded) loaded = import('../src/server.js');
  return loaded;
}

export default async function handler(req, res) {
  const mod = await loadApp();
  await mod.ensureInitialized();
  return mod.default(req, res);
}
