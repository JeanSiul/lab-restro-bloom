from pathlib import Path

server = Path('src/server.js')
text = server.read_text(encoding='utf-8')
old = """async function start() {
  // Refuse to boot in production without a strong, non-default JWT secret —
  // a weak secret would let anyone forge staff/manager sessions.
  const jwt = process.env.JWT_SECRET || '';
  if (PROD && (jwt.length < 24 || jwt === 'dev-only-change-me')) {
    console.error('FATAL: set a strong JWT_SECRET (>=24 chars) before running in production.');
    process.exit(1);
  }
  if (!PROD && jwt.length < 24) console.warn('[security] JWT_SECRET is weak/unset — fine for dev, REQUIRED in production.');
  store = await getStore();             // getStore() runs schema migration in init()
  // Auto-seed a brand-new (empty) database so fresh deploys work out of the box.
  // Existing data is never touched. Disable with AUTO_SEED=false.
  if (process.env.AUTO_SEED !== 'false') {
    const users = await store.listUsers();
    if (users.length === 0) {
      await store.reset(buildSeedData());
      console.log('  Empty database detected → seeded default menu, tables, and users.');
    }
  }
  // Self-heal: ensure the 'default' tenant has a real row (databases created
  // before multi-tenancy stored data under tenant_id='default' but had no tenants row).
  try {
    if (!(await store.getTenant(DEFAULT_TENANT))) {
      await store.createTenant({ id: DEFAULT_TENANT, name: 'Tavo', slug: DEFAULT_TENANT, plan: 'free', mode: 'restaurant', createdAt: Date.now() });
      console.log('  Backfilled the default tenant row.');
    }
  } catch (e) { console.error('default-tenant backfill skipped:', e.message); }
  app.listen(PORT, () => {
    console.log(`\\n  Tavo POS running → http://localhost:${PORT}`);
    console.log(`  Database: ${storeKind().toUpperCase()}   Payment mode: ${usingStripe ? 'STRIPE (test)' : 'MOCK (no key set)'}\\n`);
  });
}
start().catch(e => { console.error('Failed to start:', e); process.exit(1); });
"""
new = """let initPromise = null;

export function ensureInitialized() {
  if (initPromise) return initPromise;
  initPromise = (async () => {
    const jwt = process.env.JWT_SECRET || '';
    if (PROD && (jwt.length < 24 || jwt === 'dev-only-change-me')) {
      throw new Error('JWT_SECRET must be set to a strong secret (>=24 chars) in production.');
    }
    if (!PROD && jwt.length < 24) console.warn('[security] JWT_SECRET is weak/unset — fine for dev, REQUIRED in production.');
    store = await getStore();
    if (process.env.AUTO_SEED !== 'false') {
      const users = await store.listUsers();
      if (users.length === 0) {
        await store.reset(buildSeedData());
        console.log('  Empty database detected → seeded default menu, tables, and users.');
      }
    }
    try {
      if (!(await store.getTenant(DEFAULT_TENANT))) {
        await store.createTenant({ id: DEFAULT_TENANT, name: 'Tavo', slug: DEFAULT_TENANT, plan: 'free', mode: 'restaurant', createdAt: Date.now() });
        console.log('  Backfilled the default tenant row.');
      }
    } catch (e) { console.error('default-tenant backfill skipped:', e.message); }
    return store;
  })();
  return initPromise;
}

if (!process.env.VERCEL) {
  ensureInitialized()
    .then(() => app.listen(PORT, () => {
      console.log(`\\n  Tavo POS running → http://localhost:${PORT}`);
      console.log(`  Database: ${storeKind().toUpperCase()}   Payment mode: ${usingStripe ? 'STRIPE (test)' : 'MOCK (no key set)'}\\n`);
    }))
    .catch(e => { console.error('Failed to start:', e); process.exit(1); });
}

export default app;
"""
if old not in text:
    raise SystemExit('server tail pattern not found')
server.write_text(text.replace(old, new, 1), encoding='utf-8')

Path('api').mkdir(exist_ok=True)
Path('api/index.js').write_text("""// Vercel serverless adapter for the Tavo POS evaluation lab.
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
""", encoding='utf-8')

Path('vercel.json').write_text("""{
  \"version\": 2,
  \"functions\": {
    \"api/index.js\": {
      \"maxDuration\": 60
    }
  },
  \"rewrites\": [
    { \"source\": \"/api/:path*\", \"destination\": \"/api/index.js\" },
    { \"source\": \"/\", \"destination\": \"/public/index.html\" },
    { \"source\": \"/display.html\", \"destination\": \"/public/display.html\" },
    { \"source\": \"/order.html\", \"destination\": \"/public/order.html\" }
  ]
}
""", encoding='utf-8')
