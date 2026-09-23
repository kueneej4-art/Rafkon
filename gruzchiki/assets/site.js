/* Общий код для всех страниц: контакты из CONFIG, Метрика, UTM, маска телефона,
   формы заявок, всплывающее окно. Калькулятор — в wizard.js. */
(function(){
  "use strict";
  const CONFIG = window.CONFIG;
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
  const fmt = n => Math.round(n).toLocaleString("ru-RU").replace(/ /g, " ");
  const tg = (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initData) ? window.Telegram.WebApp : null;

  /* ---------- Контакты из настроек ---------- */
  $$("[data-cfg]").forEach(el => { const v = CONFIG[el.dataset.cfg]; if (v) el.textContent = v; else if ("optional" in el.dataset) el.remove(); });
  $$(".js-tel").forEach(a => a.href = "tel:" + CONFIG.phoneRaw);
  $$(".js-tel2").forEach(a => a.href = "tel:" + CONFIG.phone2Raw);
  $$(".js-tg").forEach(a => {
    if (CONFIG.telegram) a.href = "https://t.me/" + CONFIG.telegram;
    else if (a.classList.contains("m-msg")) { a.href = "tel:" + CONFIG.phoneRaw; a.removeAttribute("target"); }
    else a.style.display = "none";
  });
  /* Кнопки «Заявка через бота ВКонтакте»: открывают диалог с сообществом (vk.me),
     ref передаёт боту, откуда пришли (perevozki / gruzchiki). Пока бот не указан — страница ВК */
  $$(".js-bot").forEach(a => {
    if (CONFIG.vkBot) a.href = "https://vk.me/" + CONFIG.vkBot + "?ref=" + (a.dataset.bot || "site");
    else if (CONFIG.vk) a.href = CONFIG.vk;
    else a.style.display = "none";
  });
  $$(".js-vk").forEach(a => { if (CONFIG.vk) a.href = CONFIG.vk; else a.style.display = "none"; });
  $$(".js-wa").forEach(a => { if (CONFIG.whatsapp) a.href = "https://wa.me/" + CONFIG.whatsapp; else a.style.display = "none"; });
  const y = $("#year"); if (y) y.textContent = new Date().getFullYear();

  /* ---------- Яндекс.Метрика ---------- */
  if (CONFIG.metrikaId) {
    (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
    m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
    (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
    ym(CONFIG.metrikaId, "init", { clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true });
  }
  function goal(name, params){
    try { if (CONFIG.metrikaId && window.ym) ym(CONFIG.metrikaId, "reachGoal", name, params || {}); } catch(e){}
  }
  document.addEventListener("click", e => {
    const a = e.target.closest("[data-goal]");
    if (a) goal(a.dataset.goal);
  });

  /* ---------- UTM / yclid: откуда пришёл посетитель ---------- */
  const UTM_KEYS = ["utm_source","utm_medium","utm_campaign","utm_content","utm_term","yclid"];
  let attribution = {};
  try { attribution = JSON.parse(sessionStorage.getItem("attr") || "{}"); } catch(e){}
  const qs = new URLSearchParams(location.search);
  if (UTM_KEYS.some(k => qs.get(k))) {
    attribution = {};
    UTM_KEYS.forEach(k => { if (qs.get(k)) attribution[k] = qs.get(k); });
    try { sessionStorage.setItem("attr", JSON.stringify(attribution)); } catch(e){}
  }

  /* ---------- Маска телефона ---------- */
  function maskPhone(v){
    let d = v.replace(/\D/g, "");
    if (!d) return "";
    if (d[0] === "8") d = "7" + d.slice(1);
    if (d[0] !== "7") d = "7" + d;
    d = d.slice(0, 11);
    let out = "+7";
    if (d.length > 1) out += " (" + d.slice(1, 4);
    if (d.length >= 4) out += ")";
    if (d.length > 4) out += " " + d.slice(4, 7);
    if (d.length > 7) out += "-" + d.slice(7, 9);
    if (d.length > 9) out += "-" + d.slice(9, 11);
    return out;
  }
  function bindPhone(inp){
    inp.addEventListener("input", () => { inp.value = maskPhone(inp.value); inp.classList.remove("invalid"); });
  }
  $$('input[type="tel"]').forEach(bindPhone);

  /* ---------- Отправка заявки ---------- */
  async function sendLead(data){
    const payload = Object.assign({
      page: location.href.split("#")[0],
      referrer: document.referrer || "",
      attribution
    }, data);
    if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
      const u = tg.initDataUnsafe.user;
      payload.telegram = u.username ? "@" + u.username : String(u.id);
    }
    const r = await fetch(CONFIG.leadEndpoint, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    goal("lead", { source: payload.source });
    return true;
  }
  function failHtml(){
    return 'Не удалось отправить заявку. Пожалуйста, позвоните нам: <a href="tel:' + CONFIG.phoneRaw + '"><b>' + CONFIG.phone + '</b></a>';
  }

  /* Проверка телефона и согласия в форме; возвращает телефон или null */
  function validate(form, err){
    err.style.display = "none";
    const phoneInp = $('input[name="phone"]', form);
    if (phoneInp.value.replace(/\D/g, "").length !== 11) {
      phoneInp.classList.add("invalid"); phoneInp.focus();
      err.textContent = "Укажите номер телефона полностью, чтобы мы могли перезвонить.";
      err.style.display = "block"; return null;
    }
    const consent = $('input[name="consent"]', form);
    if (consent && !consent.checked) {
      err.textContent = "Нужно согласие на обработку персональных данных.";
      err.style.display = "block"; return null;
    }
    return phoneInp.value;
  }

  /* ---------- Всплывающее окно ---------- */
  const modal = $("#modal");
  if (modal) {
    const modalForm = $("form", modal);
    let lastFocus = null;
    const openModal = src => {
      lastFocus = document.activeElement;
      modalForm.dataset.src = src || "Всплывающая форма";
      modal.classList.add("open");
      goal("form_open", { source: modalForm.dataset.src });
      setTimeout(() => $('input[name="name"]', modal).focus(), 50);
    };
    const closeModal = () => { modal.classList.remove("open"); if (lastFocus) lastFocus.focus(); };
    $$(".js-open").forEach(b => b.addEventListener("click", e => { e.preventDefault(); openModal(b.dataset.src); }));
    $(".modal-x", modal).addEventListener("click", closeModal);
    modal.addEventListener("click", e => { if (e.target === modal) closeModal(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && modal.classList.contains("open")) closeModal(); });
  }

  /* ---------- Обычные формы заявок ---------- */
  $$("form.js-lead").forEach(form => form.addEventListener("submit", async e => {
    e.preventDefault();
    const err = $(".form-err", form);
    const phone = validate(form, err);
    if (!phone) return;
    const fd = new FormData(form);
    const btn = $('button[type="submit"]', form);
    const btnText = btn.textContent;
    btn.disabled = true; btn.textContent = "Отправляем…";
    try {
      await sendLead({
        name: (fd.get("name") || "").toString().trim(),
        phone,
        service: (fd.get("service") || "").toString(),
        comment: (fd.get("comment") || "").toString().trim(),
        source: (document.body.dataset.page ? document.body.dataset.page + " · " : "") + (form.dataset.src || "")
      });
      form.classList.add("sent");
    } catch (ex) {
      err.innerHTML = failHtml(); err.style.display = "block";
    } finally {
      btn.disabled = false; btn.textContent = btnText;
    }
  }));

  /* ---------- Плавающая кнопка «Написать сообщение» ВКонтакте ---------- */
  /* Официальный виджет VK Open API: открывает диалог с сообществом/ботом
     прямо на странице, без перехода на vk.ru. Показывается, только если
     в config.js указан vkGroupId (числовой id из vk.ru/club<id>). */
  if (CONFIG.vkGroupId && window.innerWidth >= 900) {
    const mount = () => {
      const holder = document.createElement("div");
      holder.id = "vk_community_messages";
      document.body.appendChild(holder);
      try {
        VK.Widgets.CommunityMessages("vk_community_messages", CONFIG.vkGroupId, {
          expandTimeout: 0,
          tooltipButtonText: "Задать вопрос",
        });
      } catch (e) {}
    };
    const script = document.createElement("script");
    script.src = "https://vk.com/js/api/openapi.js?169";
    script.async = true;
    script.onload = mount;
    document.head.appendChild(script);
  } // на телефоне виджет не грузим — там уже есть нижняя панель с кнопками связи

  window.Site = { CONFIG, $, $$, fmt, goal, sendLead, validate, failHtml, bindPhone, tg };
})();
