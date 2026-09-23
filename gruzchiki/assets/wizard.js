/* Пошаговый калькулятор (как в Telegram-боте): вопрос за вопросом,
   цена пересчитывается на каждом шаге, в конце — заявка в Telegram.
   Подключение: <div data-wizard="perevozki"></div> или data-wizard="gruzchiki". */
(function(){
  "use strict";
  const S = window.Site, CONFIG = window.CONFIG;
  const fmt = S.fmt;
  const CHECK = '<svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));
  const plural = (n, one, few, many) => {
    const a = n % 10, b = n % 100;
    return (a === 1 && b !== 11) ? one : (a >= 2 && a <= 4 && (b < 12 || b > 14)) ? few : many;
  };

  const WHEN = [
    { v: "today",    t: "Сегодня, срочно",  d: "подача от 30 минут, если есть свободная бригада" },
    { v: "tomorrow", t: "Завтра" },
    { v: "date",     t: "Выбрать дату",     d: "забронируем машину и бригаду заранее" },
    { v: "unknown",  t: "Пока не знаю",     d: "просто хочу узнать цену" }
  ];
  const whenText = st => st.when === "date" && st.date
    ? new Date(st.date + "T12:00").toLocaleDateString("ru-RU", { day: "numeric", month: "long", weekday: "short" })
    : (WHEN.find(w => w.v === st.when) || {}).t;

  /* ======================= Грузоперевозки ======================= */
  const P = CONFIG.perevozki;
  const PEREVOZKI = {
    source: "Калькулятор: грузоперевозки",
    init: { cargo: "move", car: "g4", route: "city", km: 100, loaders: 0, hours: 3, when: "today", date: "" },
    steps: [
      { key: "cargo", type: "single", cols: true, q: "Что нужно перевезти?",
        hint: "От этого зависит, какую машину и упаковку подобрать.",
        options: [
          { v: "move",  t: "Квартиру или комнату" },
          { v: "furn",  t: "Мебель или технику", d: "диван, шкаф, холодильник" },
          { v: "build", t: "Стройматериалы" },
          { v: "biz",   t: "Товар, оборудование", d: "для магазина, склада, офиса" },
          { v: "other", t: "Другое" }
        ] },
      { key: "car", type: "single", q: "Какая машина нужна?",
        hint: "Не уверены? Выберите примерно, менеджер подскажет точнее.",
        options: () => Object.entries(P.car).map(([v, c]) => ({ v, t: c.title, d: c.desc, p: "от " + fmt(c.hour) + " ₽/ч" })) },
      { key: "route", type: "single", q: "Куда едем?",
        options: [
          { v: "city",      t: "По Ижевску" },
          { v: "suburb",    t: "Пригород", d: "Завьялово, Ягул, Первомайский и др.", p: "+" + fmt(P.suburb) + " ₽" },
          { v: "intercity", t: "Межгород",  d: "по Удмуртии и России", p: "+" + fmt(P.km) + " ₽/км" }
        ] },
      { key: "km", type: "number", when: st => st.route === "intercity", min: 10, max: 3000, step: 10,
        q: "Сколько километров в одну сторону?",
        hint: "Примерно: Воткинск ≈ 60 км, Сарапул ≈ 65, Можга ≈ 95, Глазов ≈ 190, Пермь ≈ 290, Казань ≈ 390.",
        unit: n => n + " км" },
      { key: "loaders", type: "number", min: 0, max: 6, step: 1, q: "Нужны грузчики?",
        hint: "Водитель помогает с погрузкой, но мебель и тяжёлые вещи лучше доверить грузчикам.",
        unit: n => n ? n + " " + plural(n, "грузчик", "грузчика", "грузчиков") : "не нужны" },
      { key: "hours", type: "number", min: P.minHours, max: 12, step: 1,
        when: st => st.route !== "intercity" || st.loaders > 0,
        q: st => st.route === "intercity" ? "Сколько часов на погрузку и разгрузку?" : "Сколько часов понадобится машина?",
        hint: st => st.route === "intercity"
          ? "Время работы грузчиков на погрузке и разгрузке."
          : "Считаем от начала погрузки до конца разгрузки. Минимальный заказ " + P.minHours + " ч. Однокомнатная квартира обычно 2–3 часа.",
        unit: n => n + " ч" },
      { key: "when", type: "when", q: "Когда нужна машина?" },
      { type: "contact", q: "Ваш расчёт готов" }
    ],
    price(st) {
      const car = P.car[st.car], lines = [];
      if (st.route === "intercity") {
        lines.push([car.title + ": подача и погрузка, " + P.minHours + " ч", car.hour * P.minHours]);
        lines.push(["Дорога: " + st.km + " км × " + P.km + " ₽", st.km * P.km]);
      }
      else lines.push([car.title + " × " + st.hours + " ч", car.hour * st.hours]);
      if (st.route === "suburb") lines.push(["Выезд в пригород", P.suburb]);
      if (st.loaders) lines.push(["Грузчики: " + st.loaders + " × " + st.hours + " ч", st.loaders * P.loaderHour * st.hours]);
      return lines;
    },
    summary(st, def) {
      const o = (k, v) => def.optionsOf(k).find(x => x.v === v).t;
      return [
        ["Груз", o("cargo", st.cargo)],
        ["Машина", P.car[st.car].title],
        ["Маршрут", o("route", st.route) + (st.route === "intercity" ? ", " + st.km + " км" : "")],
        ["Грузчики", st.loaders ? st.loaders + " чел." : "не нужны"],
        (st.route !== "intercity" || st.loaders) && ["Время", st.hours + " ч"],
        ["Когда", whenText(st)]
      ].filter(Boolean);
    }
  };

  /* ======================= Грузчики ======================= */
  const G = CONFIG.gruzchiki;
  const GRUZCHIKI = {
    source: "Калькулятор: грузчики",
    init: { work: "load", loaders: 2, hours: 3, floor: "lift", extras: [], when: "today", date: "" },
    steps: [
      { key: "work", type: "single", cols: true, q: "Какая работа нужна?",
        options: [
          { v: "load",  t: "Погрузка / разгрузка", d: "машины, фуры, контейнера" },
          { v: "move",  t: "Помощь при переезде" },
          { v: "build", t: "Подъём стройматериалов", d: "гипсокартон, мешки, плитка" },
          { v: "furn",  t: "Перестановка мебели" },
          { v: "heavy", t: "Пианино, сейф, тяжёлое", d: "такелажные работы", p: "+" + fmt(G.heavy) + " ₽" },
          { v: "trash", t: "Вынос мусора, старой мебели" },
          { v: "labor", t: "Разнорабочие", d: "демонтаж, уборка, подсобные работы" }
        ] },
      { key: "loaders", type: "number", min: 1, max: 10, step: 1, q: "Сколько нужно грузчиков?",
        hint: "Для однокомнатной квартиры обычно хватает 2 человек, для фуры 3–4.",
        unit: n => n + " " + plural(n, "грузчик", "грузчика", "грузчиков") },
      { key: "hours", type: "number", min: G.minHours, max: 12, step: 1, q: "Сколько часов займёт работа?",
        hint: "Минимальный заказ " + G.minHours + " ч. Если работа закончится раньше, за лишнее время не платите.",
        unit: n => n + " ч" },
      { key: "floor", type: "single", q: "Этаж и лифт",
        options: [
          { v: "lift", t: "Есть лифт или 1 этаж" },
          { v: "mid",  t: "2–4 этаж без лифта", p: "+" + fmt(G.floorMid) + " ₽/чел." },
          { v: "high", t: "5 этаж и выше без лифта", p: "+" + fmt(G.floorHigh) + " ₽/чел." }
        ] },
      { key: "extras", type: "multi", q: "Что-то ещё?", hint: "Можно выбрать несколько или пропустить.",
        options: [
          { v: "furn",  t: "Разборка и сборка мебели", p: "+" + fmt(G.furn) + " ₽" },
          { v: "pack",  t: "Упаковка вещей", d: "стрейч, картон, пузырчатая плёнка", p: "+" + fmt(G.pack) + " ₽" },
          { v: "gazel", t: "Нужна газель", d: "машина с водителем на то же время", p: fmt(G.gazelHour) + " ₽/ч" }
        ] },
      { key: "when", type: "when", q: "Когда нужны грузчики?" },
      { type: "contact", q: "Ваш расчёт готов" }
    ],
    price(st) {
      const lines = [["Грузчики: " + st.loaders + " × " + st.hours + " ч", st.loaders * G.loaderHour * st.hours]];
      if (st.work === "heavy") lines.push(["Такелаж", G.heavy]);
      if (st.floor === "mid")  lines.push(["Без лифта, 2–4 этаж", G.floorMid * st.loaders]);
      if (st.floor === "high") lines.push(["Без лифта, 5+ этаж", G.floorHigh * st.loaders]);
      if (st.extras.includes("furn"))  lines.push(["Разборка/сборка мебели", G.furn]);
      if (st.extras.includes("pack"))  lines.push(["Упаковка", G.pack]);
      if (st.extras.includes("gazel")) lines.push(["Газель × " + st.hours + " ч", G.gazelHour * st.hours]);
      return lines;
    },
    summary(st, def) {
      const o = (k, v) => def.optionsOf(k).find(x => x.v === v).t;
      const ex = st.extras.map(v => o("extras", v));
      return [
        ["Работа", o("work", st.work)],
        ["Грузчики", st.loaders + " чел. × " + st.hours + " ч"],
        ["Этаж", o("floor", st.floor)],
        ex.length && ["Дополнительно", ex.join(", ")],
        ["Когда", whenText(st)]
      ].filter(Boolean);
    }
  };

  const DEFS = { perevozki: PEREVOZKI, gruzchiki: GRUZCHIKI };

  /* ======================= Движок ======================= */
  function mount(root, def) {
    const st = JSON.parse(JSON.stringify(def.init));
    let idx = 0, sent = false;
    const val = (x) => typeof x === "function" ? x(st) : x;
    def.optionsOf = k => val(def.steps.find(s => s.key === k).options);
    const active = () => def.steps.filter(s => !s.when || s.when(st));
    const total = () => def.price(st).reduce((a, l) => a + l[1], 0);
    let started = false;
    const touch = () => { if (!started) { started = true; S.goal("calc_start", { calc: def.source }); } };

    function go(d) {
      const list = active(), cur = list[idx];
      const next = list.indexOf(cur) + d;
      idx = Math.max(0, Math.min(active().length - 1, next));
      render(true);
    }

    function optBtn(o, selected, multi) {
      return '<button type="button" class="wiz-opt' + (multi ? " multi" : "") + (selected ? " sel" : "") + '" data-v="' + esc(o.v) + '" aria-pressed="' + selected + '">' +
        '<span class="ck">' + CHECK + '</span><span class="m"><span class="t">' + esc(o.t) + '</span>' +
        (o.d ? '<span class="d">' + esc(o.d) + '</span>' : "") + '</span>' +
        (o.p ? '<span class="p">' + esc(o.p) + '</span>' : "") + '</button>';
    }

    function render(focus) {
      if (sent) return;
      const list = active();
      if (idx >= list.length) idx = list.length - 1;
      const step = list[idx], n = list.length, last = step.type === "contact";
      let body = "";

      if (step.type === "single" || step.type === "multi") {
        const opts = val(step.options);
        body = '<div class="wiz-opts' + (step.cols ? " cols" : "") + '">' +
          opts.map(o => optBtn(o, step.type === "multi" ? st[step.key].includes(o.v) : st[step.key] === o.v, step.type === "multi")).join("") + '</div>';
      } else if (step.type === "number") {
        body = '<div class="wiz-num"><button type="button" data-d="-1" aria-label="Меньше">−</button>' +
          '<output aria-live="polite">' + esc(step.unit(st[step.key])) + '</output>' +
          '<button type="button" data-d="1" aria-label="Больше">+</button></div>' +
          (step.key === "km" ? '<p style="margin-top:14px"><input class="wiz-input" type="number" inputmode="numeric" min="' + step.min + '" max="' + step.max + '" value="' + st.km + '" aria-label="Километры"></p>' : "");
      } else if (step.type === "when") {
        body = '<div class="wiz-opts cols">' + WHEN.map(o => optBtn(o, st.when === o.v)).join("") + '</div>' +
          (st.when === "date" ? '<p style="margin-top:14px"><input class="wiz-input" type="date" value="' + esc(st.date) + '" min="' + new Date().toISOString().slice(0, 10) + '" aria-label="Дата"></p>' : "");
      } else if (step.type === "contact") {
        const lines = def.price(st);
        body = '<ul class="wiz-sum">' + def.summary(st, def).map(([a, b]) => '<li><span>' + esc(a) + '</span><span>' + esc(b) + '</span></li>').join("") + '</ul>' +
          '<div class="wiz-total"><small>Ориентировочная стоимость</small><b>≈ ' + fmt(total()) + ' ₽</b>' +
          '<div style="font-size:13px;color:var(--ink-soft);margin-top:4px">' + lines.map(l => esc(l[0]) + ": " + fmt(l[1]) + " ₽").join(" · ") + '</div></div>' +
          '<form class="wiz-form" novalidate>' +
          '<div class="gift"><svg><use href="#i-gift"/></svg> <span>' + esc(CONFIG.offer) + '</span></div>' +
          '<label class="field"><span>Ваше имя</span><input name="name" autocomplete="given-name" placeholder="Как к вам обращаться" value="' + esc(st.name || "") + '"></label>' +
          '<label class="field"><span>Телефон *</span><input name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" required value="' + esc(st.phone || "") + '"></label>' +
          '<label class="field"><span>Комментарий</span><input name="comment" placeholder="Адреса, что везём, пожелания" value="' + esc(st.comment || "") + '"></label>' +
          '<button class="btn btn-accent btn-block" type="submit">Зафиксировать цену</button>' +
          '<label class="consent"><input type="checkbox" name="consent" checked required> <span>Согласен на обработку персональных данных согласно <a href="privacy.html" target="_blank">политике конфиденциальности</a></span></label>' +
          '<div class="form-err" role="alert"></div>' +
          '<p style="font-size:13px;color:var(--ink-soft);margin-top:10px">Менеджер перезвонит, уточнит детали и закрепит точную цену в договоре.</p></form>';
      }

      const q = val(step.q), hint = val(step.hint);
      root.innerHTML =
        '<div class="wiz-head"><span>' + (last ? "Готово" : "Шаг " + (idx + 1) + " из " + (n - 1)) + '</span>' +
        (!last ? '<span>≈ <b style="color:var(--ink)">' + fmt(total()) + ' ₽</b></span>' : "") + '</div>' +
        '<div class="wiz-ticks">' + list.map((_, i) => '<i class="' + (i <= idx ? "on" : "") + '"></i>').join("") + '</div>' +
        '<h3 class="wiz-q" tabindex="-1">' + esc(q) + '</h3>' + (hint ? '<p class="wiz-hint">' + esc(hint) + '</p>' : '<div style="height:12px"></div>') +
        body +
        '<div class="wiz-nav">' + (idx > 0 ? '<button type="button" class="btn back" data-nav="-1" aria-label="Назад">←</button>' : "") +
        (!last ? '<button type="button" class="btn btn-accent" data-nav="1">' + (step.type === "multi" && !st[step.key].length ? "Пропустить" : "Далее") + '</button>' : "") + '</div>';

      bind(step);
      if (focus) { const h = root.querySelector(".wiz-q"); h && h.focus({ preventScroll: true }); if (root.getBoundingClientRect().top < 0) root.scrollIntoView({ behavior: "smooth", block: "start" }); }
    }

    function bind(step) {
      root.querySelectorAll("[data-nav]").forEach(b => b.onclick = () => go(+b.dataset.nav));
      root.querySelectorAll(".wiz-opt").forEach(b => b.onclick = () => {
        touch();
        const v = b.dataset.v;
        if (step.type === "multi") {
          const a = st[step.key], i = a.indexOf(v);
          i >= 0 ? a.splice(i, 1) : a.push(v);
          render();
        } else {
          st[step.type === "when" ? "when" : step.key] = v;
          if (step.type === "when" && v === "date") { render(); const d = root.querySelector('input[type="date"]'); d && d.focus(); return; }
          render();
          setTimeout(() => go(1), 180);   // как в боте: выбрал — сразу следующий вопрос
        }
      });
      root.querySelectorAll(".wiz-num button").forEach(b => b.onclick = () => {
        touch();
        st[step.key] = Math.max(step.min, Math.min(step.max, st[step.key] + (+b.dataset.d) * step.step));
        render();
      });
      const km = root.querySelector('.wiz-input[type="number"]');
      if (km) km.onchange = () => { const v = parseInt(km.value, 10); if (v > 0) st.km = Math.max(step.min, Math.min(step.max, v)); render(); };
      const date = root.querySelector('input[type="date"]');
      if (date) date.onchange = () => { st.date = date.value; render(); };

      const form = root.querySelector(".wiz-form");
      if (form) {
        form.querySelectorAll('input[type="tel"]').forEach(S.bindPhone);
        form.querySelectorAll("input[name]").forEach(i => i.addEventListener("input", () => { st[i.name] = i.value; }));
        form.onsubmit = async e => {
          e.preventDefault();
          const err = form.querySelector(".form-err");
          const phone = S.validate(form, err);
          if (!phone) return;
          const btn = form.querySelector('button[type="submit"]');
          btn.disabled = true; btn.textContent = "Отправляем…";
          const lines = def.price(st);
          const calc = def.summary(st, def).map(([a, b]) => a + ": " + b).join("\n") +
            "\n" + lines.map(l => l[0] + " = " + fmt(l[1]) + " ₽").join("\n") + "\nИтого ≈ " + fmt(total()) + " ₽";
          try {
            await S.sendLead({ name: form.name.value.trim(), phone, comment: form.comment.value.trim(), source: def.source, calc });
            sent = true;
            root.innerHTML = '<div class="form-ok" role="status" style="display:block"><svg><use href="#i-check"/></svg>' +
              '<h3>Заявка отправлена!</h3><p class="muted">Перезвоним в течение 5–10 минут и подтвердим стоимость ≈ ' + fmt(total()) + ' ₽.</p></div>';
            if (S.tg) setTimeout(() => { try { S.tg.close(); } catch (x) {} }, 2500);
          } catch (ex) {
            err.innerHTML = S.failHtml(); err.style.display = "block";
            btn.disabled = false; btn.textContent = "Зафиксировать цену";
          }
        };
      }
    }

    render();
  }

  document.querySelectorAll("[data-wizard]").forEach(el => {
    const def = DEFS[el.dataset.wizard];
    if (def) mount(el, def);
  });
  if (S.tg) { try { S.tg.ready(); S.tg.expand(); } catch (e) {} }
})();
