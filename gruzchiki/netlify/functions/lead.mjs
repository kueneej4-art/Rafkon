// Принимает заявку с сайта и пересылает её в Telegram.
// Переменные окружения (Netlify → Site configuration → Environment variables):
//   TELEGRAM_BOT_TOKEN — токен бота от @BotFather
//   TELEGRAM_CHAT_ID   — id чата/группы, куда слать заявки (можно несколько через запятую)

const esc = (s) => String(s ?? "").replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])).slice(0, 1000);

export default async (req) => {
  if (req.method !== "POST") return new Response("Method Not Allowed", { status: 405 });

  let d;
  try { d = await req.json(); } catch { return new Response("Bad JSON", { status: 400 }); }

  const digits = String(d.phone || "").replace(/\D/g, "");
  if (digits.length !== 11) return new Response("Bad phone", { status: 400 });

  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chats = (process.env.TELEGRAM_CHAT_ID || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (!token || !chats.length) return new Response("Server not configured", { status: 500 });

  const a = d.attribution || {};
  const lines = [
    "🚚 <b>Новая заявка с сайта</b>",
    "",
    `📞 <b>${esc(d.phone)}</b>`,
    d.name ? `👤 ${esc(d.name)}` : null,
    d.service ? `📦 ${esc(d.service)}` : null,
    d.comment ? `💬 ${esc(d.comment)}` : null,
    d.calc ? `🧮 ${esc(d.calc)}` : null,
    "",
    `Форма: ${esc(d.source)}`,
    (a.utm_source || a.yclid) ? `Источник: ${esc([a.utm_source, a.utm_medium, a.utm_campaign].filter(Boolean).join(" / ") || "Яндекс.Директ")}` : null,
    a.utm_term ? `Ключевая фраза: ${esc(a.utm_term)}` : null,
    a.utm_content ? `Объявление: ${esc(a.utm_content)}` : null,
    a.yclid ? `yclid: ${esc(a.yclid)}` : null,
  ].filter((x) => x !== null);

  const results = await Promise.all(chats.map((chat_id) =>
    fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id, text: lines.join("\n"), parse_mode: "HTML", disable_web_page_preview: true }),
    }).then((r) => r.ok).catch(() => false)
  ));

  if (!results.some(Boolean)) return new Response("Telegram error", { status: 502 });
  return Response.json({ ok: true });
};
