import fetch from "node-fetch";
import { URLSearchParams } from "url";

const backend = "http://localhost:8000";
const frontend = "http://localhost:5176";

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function run() {
  const username = `ui_smoke_${Date.now()}`;
  const password = "TestPass123";
  console.log("username:", username);

  // register
  let res = await fetch(`${backend}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  console.log("/auth/register", res.status);
  const regBody = await res.text();
  console.log("reg body:", regBody);

  // login (form)
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);
  res = await fetch(`${backend}/auth/login`, { method: "POST", body: params });
  console.log("/auth/login", res.status);
  const login = await res.json();
  if (!login.access_token) {
    console.error("no token");
    process.exit(2);
  }
  const token = login.access_token;
  console.log("got token (truncated):", token.slice(0, 20) + "...");

  // extract user id from token
  const parts = token.split(".");
  const payload = JSON.parse(
    Buffer.from(
      parts[1].padEnd(parts[1].length + ((4 - (parts[1].length % 4)) % 4), "="),
      "base64",
    ).toString(),
  );
  const userId = payload.sub;
  console.log("user id:", userId);

  // create expense
  res = await fetch(`${backend}/expenses`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      amount: 12.34,
      category_id: "smoke-cat",
      date: new Date().toISOString(),
    }),
  });
  console.log("POST /expenses", res.status);
  const created = await res.json();
  console.log("created expense id:", created._id || JSON.stringify(created));

  // fetch expenses
  res = await fetch(`${backend}/expenses/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  console.log("GET /expenses", res.status);
  const exps = await res.json();
  console.log(
    "expenses count:",
    Array.isArray(exps) ? exps.length : "unexpected",
  );

  // request frontend root
  try {
    res = await fetch(frontend);
    console.log("frontend root", res.status);
    const text = await res.text();
    console.log("frontend root length:", text.length);
  } catch (e) {
    console.error("frontend fetch error:", e.message);
  }

  console.log("smoke test complete");
}

run().catch((e) => {
  console.error(e);
  process.exit(1);
});
