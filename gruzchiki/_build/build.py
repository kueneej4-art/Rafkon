#!/usr/bin/env python3
"""Собирает страницы сайта из общих кусков (шапка, подвал, формы)."""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent
SCR = pathlib.Path(__file__).parent
sprite = (SCR / "sprite.html").read_text()
sprite = sprite.replace("</svg>", """  <symbol id="i-evac" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" d="M2 17V13h9l2-4h4l3 4v4M2 13l8-7M10 6l2 3M6 17h8"/><circle cx="6" cy="17.5" r="2" fill="currentColor"/><circle cx="17" cy="17.5" r="2" fill="currentColor"/></symbol>
  <symbol id="i-wa" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.8 11.8 0 004.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 001.8-1.2 2.2 2.2 0 00.1-1.2c0-.1-.2-.2-.4-.3z"/></symbol>
</svg>""", 1)

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23FFCC00'/%3E"
        "%3Cpath d='M6 11h12v10H6zM18 14h5l3 4v3h-8z' fill='%231D1D1F'/%3E%3Ccircle cx='10' cy='22' r='2.5' fill='%23fff'/%3E%3Ccircle cx='22' cy='22' r='2.5' fill='%23fff'/%3E%3C/svg%3E")


def head(title, desc, extra=""):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FBFBFD" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="img/gazel.jpg">
<link rel="icon" href="{ICON}">
{FONT}
<link rel="stylesheet" href="assets/style.css">
{extra}</head>
"""


def header(active):
    def a(href, text, key):
        cls = ' class="active" aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cls}>{text}</a>'
    return f"""<header class="top">
  <div class="wrap top-in">
    <a class="logo" href="index.html" aria-label="На главную">
      <span class="logo-mark"><svg><use href="#i-truck"/></svg></span>
      <span><span data-cfg="brand">Переезды по Ижевску</span><small><span data-cfg="person">Денис Ларин</span> · грузоперевозки</small></span>
    </a>
    <nav class="top-nav" aria-label="Разделы">
      {a("index.html", "Главная", "home")}
      {a("perevozki.html", "Грузоперевозки", "perevozki")}
      {a("gruzchiki.html", "Грузчики", "gruzchiki")}
      {a("index.html#prices", "Цены", "prices")}
      {a("#contacts", "Контакты", "contacts")}
    </nav>
    <div class="top-phone">
      <a class="tel js-tel" href="tel:+73412565632" data-goal="phone_click"><span data-cfg="phone">56-56-32</span></a>
      <button class="btn btn-accent js-open" data-src="Шапка: перезвоните" type="button">Перезвоните мне</button>
    </div>
  </div>
</header>
"""


def trust():
    return """<div class="trust">
  <div class="wrap trust-grid">
    <div><b>30 мин</b><span>подача по Ижевску</span></div>
    <div><b>4 и 6 м</b><span>газели в работе</span></div>
    <div><b>10+ лет</b><span>на рынке Ижевска</span></div>
    <div><b>7,6 тыс.</b><span>подписчиков ВКонтакте</span></div>
  </div>
</div>
"""


def pains():
    return """<section class="dark-sec">
  <div class="wrap center">
    <span class="eyebrow">Почему мы</span>
    <h2>Всё, чего вы боитесь,<br>у нас не случится.</h2>
  </div>
  <div class="wrap">
    <div class="pains">
      <div class="pain"><div class="no">«На месте цена вырастет в два раза»</div><div class="yes">Называем стоимость заранее, по телефону. Доплата только за то, что вы сами добавили к заказу.</div></div>
      <div class="pain"><div class="no">«Придётся ждать полдня»</div><div class="yes">Подача от 30 минут по Ижевску. Или приедем точно к тому времени, на которое договорились.</div></div>
      <div class="pain"><div class="no">«Поцарапают мебель и разобьют посуду»</div><div class="yes">Упаковываем, крепим груз ремнями, аккуратно носим. Больше 10 лет перевозим вещи ижевчан.</div></div>
      <div class="pain"><div class="no">«Приедут случайные люди»</div><div class="yes">Своя машина и своя бригада. Денис Ларин лично отвечает за каждый заказ и всегда на связи.</div></div>
    </div>
  </div>
</section>
"""


def about():
    return """<section id="about">
  <div class="wrap about">
    <figure class="about-photo"><img src="img/gazel.jpg" alt="Денис Ларин у своей газели" width="768" height="1024" loading="lazy"><figcaption><b>Денис Ларин</b>руководитель, лично отвечает за каждый заказ</figcaption></figure>
    <div>
      <span class="eyebrow y">Денис Ларин — Легенда</span>
      <h2>Не диспетчерская.<br>Своя машина и своя бригада.</h2>
      <p>Многие «компании» по грузоперевозкам просто перепродают заказы случайным водителям. Никто не знает, кто приедет и в каком состоянии.</p>
      <p>У нас иначе: больше 10 лет работаем на своих газелях, грузчиков знаем лично, а на связи с вами сам руководитель.</p>
      <ul>
        <li><svg><use href="#i-check"/></svg> Газели 4 и 6 метров, эвакуатор</li>
        <li><svg><use href="#i-check"/></svg> Свои грузчики и разнорабочие</li>
        <li><svg><use href="#i-check"/></svg> Денис на связи в Telegram, WhatsApp и ВКонтакте</li>
        <li><svg><use href="#i-check"/></svg> 7,6 тыс. подписчиков ВКонтакте: нас знают в Ижевске</li>
      </ul>
      <div class="cta-row">
        <button class="btn btn-accent js-open" type="button" data-src="Кто мы: заказать">Заказать</button>
        <a class="more js-vk" href="https://vk.ru/denislarin30" target="_blank" rel="noopener" data-goal="messenger_click">Мы во ВКонтакте</a>
      </div>
    </div>
  </div>
</section>
"""


def steps(cls=""):
    return f"""<section class="{cls}">
  <div class="wrap center">
    <span class="eyebrow">Как мы работаем</span>
    <h2>Четыре простых шага.</h2>
  </div>
  <div class="wrap">
    <div class="steps">
      <div class="step"><h3>Звонок или заявка</h3><p>Звоните на 56-56-32 или оставляете заявку. Перезваниваем за 5–10 минут.</p></div>
      <div class="step"><h3>Цена заранее</h3><p>Уточняем объём, этажи и адреса. Называем стоимость до начала работ.</p></div>
      <div class="step"><h3>Подача от 30 минут</h3><p>Машина и бригада приезжают вовремя: грузим, везём, заносим.</p></div>
      <div class="step"><h3>Оплата по факту</h3><p>Платите, когда всё на месте и вы всё проверили.</p></div>
    </div>
  </div>
</section>
"""


def faq(items, cls=""):
    body = "\n".join(f"      <details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    return f"""<section id="faq" class="{cls}">
  <div class="wrap center">
    <span class="eyebrow">Вопросы</span>
    <h2>Частые вопросы.</h2>
  </div>
  <div class="wrap">
    <div class="faq">
{body}
    </div>
  </div>
</section>
"""


def contacts(page_label, service_default, cls="alt"):
    opts = ["Квартирный переезд", "Газель с водителем", "Грузчики", "Разнорабочие", "Эвакуатор", "Другое"]
    options = "".join(f"<option{' selected' if o == service_default else ''}>{o}</option>" for o in opts)
    return f"""<section class="{cls}" id="contacts">
  <div class="wrap final-grid">
    <div>
      <span class="eyebrow">Контакты</span>
      <h2>Звоните.<br>Подача от 30 минут.</h2>
      <p class="lead-text">Консультация бесплатная: подскажем, какая машина и сколько грузчиков нужно, чтобы вы не переплатили.</p>
      <div class="contacts">
        <a class="js-tel" href="tel:+73412565632" data-goal="phone_click"><span class="ci"><svg><use href="#i-phone"/></svg></span><span><span data-cfg="phone">56-56-32</span><small>городской</small></span></a>
        <a class="js-mob" href="tel:+79127681545" data-goal="phone_click"><span class="ci"><svg><use href="#i-phone"/></svg></span><span><span data-cfg="mobile">8-912-768-15-45</span><small>мобильный</small></span></a>
        <a class="js-wa" href="https://wa.me/79127681545" data-goal="messenger_click" target="_blank" rel="noopener"><span class="ci"><svg><use href="#i-wa"/></svg></span><span>WhatsApp<small>напишите, ответим быстро</small></span></a>
        <a class="js-tg" href="https://t.me/vladospa" data-goal="messenger_click" target="_blank" rel="noopener"><span class="ci"><svg><use href="#i-tg"/></svg></span><span>Telegram</span></a>
        <a class="js-vk" href="https://vk.ru/denislarin30" data-goal="messenger_click" target="_blank" rel="noopener"><span class="ci"><svg><use href="#i-vk"/></svg></span><span>ВКонтакте</span></a>
        <div><span class="ci"><svg><use href="#i-pin"/></svg></span><span><span data-cfg="address">Ижевск, ул. Орджоникидзе, 13</span></span></div>
      </div>
    </div>
    <form class="card js-lead" data-src="Контакты: форма" novalidate>
      <div class="form-body">
        <h3>Оставьте заявку.</h3>
        <p class="muted">Перезвоним в течение 5–10 минут и назовём цену.</p>
        <label class="field"><span>Ваше имя</span><input name="name" autocomplete="given-name" placeholder="Как к вам обращаться"></label>
        <label class="field"><span>Телефон *</span><input name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" required></label>
        <label class="field"><span>Что нужно</span><select name="service">{options}</select></label>
        <label class="field"><span>Комментарий</span><textarea name="comment" placeholder="Откуда и куда, что везём, желаемая дата"></textarea></label>
        <button class="btn btn-accent btn-block" type="submit">Отправить заявку</button>
        <label class="consent"><input type="checkbox" name="consent" checked required> <span>Согласен на обработку персональных данных согласно <a href="privacy.html" target="_blank">политике конфиденциальности</a></span></label>
        <div class="form-err" role="alert"></div>
      </div>
      <div class="form-ok" role="status">
        <svg><use href="#i-check"/></svg>
        <h3>Заявка у нас!</h3>
        <p class="muted">Перезвоним в течение 5–10 минут. Срочно? Звоните: <a class="js-tel" href="tel:+73412565632" data-goal="phone_click"><b data-cfg="phone">56-56-32</b></a></p>
      </div>
    </form>
  </div>
</section>
"""


def tail(wizard=False):
    wz = '\n<script src="assets/wizard.js"></script>' if wizard else ""
    return f"""
<footer>
  <div class="wrap">
    <div>© <span id="year"></span> <span data-cfg="brand">Переезды по Ижевску</span> · <span data-cfg="person">Денис Ларин</span> · <span data-cfg="address">Ижевск, ул. Орджоникидзе, 13</span> <span data-cfg="legal" data-optional></span></div>
    <nav><a href="perevozki.html">Грузоперевозки</a><a href="gruzchiki.html">Грузчики</a><a href="privacy.html">Политика конфиденциальности</a></nav>
  </div>
</footer>

<nav class="mbar" aria-label="Быстрая связь">
  <a class="m-call js-tel" href="tel:+73412565632" data-goal="phone_click"><svg><use href="#i-phone"/></svg> Звонок</a>
  <a class="m-msg js-wa" href="https://wa.me/79127681545" data-goal="messenger_click" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg> WhatsApp</a>
  <button class="m-lead js-open" data-src="Моб. панель: узнать цену" type="button">Узнать цену</button>
</nav>

<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
  <form class="card js-lead" data-src="Всплывающая форма" novalidate>
    <button class="modal-x" type="button" aria-label="Закрыть">×</button>
    <div class="form-body">
      <h3 id="modalTitle">Перезвоним за 5 минут.</h3>
      <p class="muted">Назовём цену и ответим на вопросы.</p>
      <label class="field"><span>Ваше имя</span><input name="name" autocomplete="given-name" placeholder="Как к вам обращаться"></label>
      <label class="field"><span>Телефон *</span><input name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" required></label>
      <button class="btn btn-accent btn-block" type="submit">Жду звонка</button>
      <label class="consent"><input type="checkbox" name="consent" checked required> <span>Согласен с <a href="privacy.html" target="_blank">политикой конфиденциальности</a></span></label>
      <div class="form-err" role="alert"></div>
    </div>
    <div class="form-ok" role="status">
      <svg><use href="#i-check"/></svg>
      <h3>Заявка принята!</h3>
      <p class="muted">Перезвоним в течение 5–10 минут.</p>
    </div>
  </form>
</div>

<script src="assets/config.js"></script>
<script src="assets/site.js"></script>{wz}
</body>
</html>
"""


def calc_section(kind, title, lead, cls="alt"):
    return f"""<section id="calc" class="{cls}">
  <div class="wrap center">
    <span class="eyebrow y">Калькулятор</span>
    <h2>{title}</h2>
    <p class="lead-text">{lead}</p>
  </div>
  <div class="wrap">
    <div class="wiz-wrap">
      <div class="wiz" data-wizard="{kind}" aria-live="polite"></div>
      <aside class="wiz-side">
        <div class="card">
          <h3>Проще позвонить?</h3>
          <a class="big js-tel" href="tel:+73412565632" data-goal="phone_click" data-cfg="phone">56-56-32</a>
          <p style="color:var(--ink-soft);font-size:15px;margin-top:6px">Посчитаем по телефону за пару минут.</p>
        </div>
        <div class="card">
          <h3>Что входит в цену</h3>
          <ul>
            <li><svg><use href="#i-check"/></svg> Подача к подъезду от 30 минут</li>
            <li><svg><use href="#i-check"/></svg> Ремни и крепление груза</li>
            <li><svg><use href="#i-check"/></svg> Стоимость называем до начала работ</li>
            <li><svg><use href="#i-check"/></svg> Оплата после выполнения</li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</section>
"""


def svc(icon, title, text, price, src):
    return f"""      <article class="svc">
        <div class="svc-ico"><svg><use href="#i-{icon}"/></svg></div>
        <h3>{title}</h3>
        <p>{text}</p>
        <div class="price"><b>{price}</b><a href="#" class="js-open" data-src="Услуга: {src}">Заказать ›</a></div>
      </article>"""


def services(eyebrow, title, items, cls=""):
    return f"""<section id="services" class="{cls}">
  <div class="wrap center">
    <span class="eyebrow">{eyebrow}</span>
    <h2>{title}</h2>
  </div>
  <div class="wrap">
    <div class="grid g3">
{chr(10).join(svc(*i) for i in items)}
    </div>
  </div>
</section>
"""


def ptable(rows, note, cls=""):
    body = "\n".join(f'      <div class="prow"><div>{a}<small>{b}</small></div><b>{c}</b></div>' for a, b, c in rows)
    return f"""<section id="prices" class="{cls}">
  <div class="wrap center">
    <span class="eyebrow">Цены</span>
    <h2>Честные цены.</h2>
    <p class="lead-text">Стоимость называем заранее, до начала работ.</p>
  </div>
  <div class="wrap" style="max-width:820px">
    <div class="ptable">
{body}
    </div>
    <p class="price-note">{note}</p>
  </div>
</section>
"""


def hero(eyebrow, h1, lead, cta_href, cta_text, note):
    return f"""<section class="hero">
  <div class="wrap">
    <span class="eyebrow y">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead-text">{lead}</p>
    <div class="cta-row">
      <a class="btn btn-accent" href="{cta_href}">{cta_text}</a>
      <a class="btn btn-ghost js-tel" href="tel:+73412565632" data-goal="phone_click"><svg><use href="#i-phone"/></svg> <span data-cfg="phone">56-56-32</span></a>
    </div>
    <p class="hero-note">{note}</p>
  </div>
  <div class="wrap"><div class="hero-photo"><img src="img/gazel.jpg" alt="Газель компании и Денис Ларин" width="768" height="1024" fetchpriority="high"></div></div>
</section>
"""


FAQ_COMMON = [
    ("Как быстро вы приедете?", "По Ижевску подача от 30 минут, если есть свободная машина или бригада. На выходные и конец месяца лучше бронировать заранее."),
    ("Может ли цена измениться на месте?", "Стоимость называем заранее. Меняется она только если вы сами добавите работу, например решите вывезти ещё и гараж."),
    ("Как оплатить?", "По факту, после выполнения работы. Наличными или переводом."),
]

# ============================ Главная ============================
index = head("Переезды по Ижевску: газели, грузчики, эвакуатор · Денис Ларин",
             "Грузоперевозки и грузчики в Ижевске. Газели 4 и 6 м от 1500 ₽/час, грузчики от 700 ₽/час, эвакуатор от 2500 ₽. Подача от 30 минут. Тел. 56-56-32.")
index += '<body data-page="Главная">\n' + sprite + "\n" + header("home") + '<main id="top">\n'
index += hero("Денис Ларин · грузоперевозки",
              'Переезды<br>по Ижевску.',
              "Газели 4 и 6 метров, грузчики, эвакуатор.<br>Подача от 30 минут.",
              "#dirs", "Рассчитать стоимость", "Звоните: ответим сразу и назовём цену")
index += trust()
index += """<section class="alt" id="prices">
  <div class="wrap center">
    <span class="eyebrow">Цены</span>
    <h2>Просто и честно.</h2>
    <p class="lead-text">Стоимость называем до начала работ. Никаких сюрпризов на месте.</p>
  </div>
  <div class="wrap">
    <div class="tiles">
      <div class="tile"><div class="svc-ico"><svg><use href="#i-truck"/></svg></div><h3>Газель</h3><div class="big">от 1500 ₽<small> /час</small></div><p>Газели 4 и 6 метров с водителем.</p><a class="more" href="perevozki.html">Рассчитать перевозку</a></div>
      <div class="tile"><div class="svc-ico"><svg><use href="#i-people"/></svg></div><h3>Грузчик</h3><div class="big">от 700 ₽<small> /час</small></div><p>Грузчики и разнорабочие.</p><a class="more" href="gruzchiki.html">Рассчитать грузчиков</a></div>
      <div class="tile"><div class="svc-ico"><svg><use href="#i-evac"/></svg></div><h3>Эвакуатор</h3><div class="big">от 2500 ₽</div><p>Эвакуация легковых автомобилей.</p><a class="more js-open" href="#" data-src="Эвакуатор">Вызвать эвакуатор</a></div>
    </div>
  </div>
</section>

<section id="dirs">
  <div class="wrap center">
    <span class="eyebrow">Что вам нужно?</span>
    <h2>Выберите услугу.</h2>
    <p class="lead-text">У каждой свой калькулятор: ответьте на несколько вопросов и сразу увидите цену.</p>
  </div>
  <div class="wrap">
    <div class="dirs">
      <a class="dir d1" href="perevozki.html#calc">
        <span class="k">Машина с водителем</span>
        <h3>Грузоперевозки</h3>
        <p>Переезды, мебель, техника, стройматериалы, межгород. Газели 4 и 6 м.</p>
        <span class="go">Рассчитать перевозку ›</span>
        <svg class="bgi"><use href="#i-truck"/></svg>
      </a>
      <a class="dir d2" href="gruzchiki.html#calc">
        <span class="k">Крепкие руки</span>
        <h3>Грузчики</h3>
        <p>Погрузка, разгрузка, подъём на этаж, такелаж, разнорабочие.</p>
        <span class="go">Рассчитать грузчиков ›</span>
        <svg class="bgi"><use href="#i-people"/></svg>
      </a>
    </div>
  </div>
</section>
"""
index += pains() + about() + steps("alt")
index += faq(FAQ_COMMON + [
    ("Какие машины у вас есть?", "Газели 4 и 6 метров, а также эвакуатор. Подберём машину под ваш объём, чтобы не переплачивать за пустой кузов."),
    ("Вы разбираете и собираете мебель?", "Да, у бригады есть инструмент: разберём шкафы и кровати, а на новом месте соберём."),
])
index += contacts("Главная", "Квартирный переезд")
index += "</main>\n" + tail()
(OUT / "index.html").write_text(index)

# ============================ Грузоперевозки ============================
pv = head("Грузоперевозки в Ижевске: газели 4 и 6 м от 1500 ₽/час · подача 30 минут",
          "Газель с водителем в Ижевске: переезды, мебель, стройматериалы, межгород. Газели 4 и 6 метров от 1500 ₽/час. Подача от 30 минут. Рассчитайте стоимость онлайн.")
pv += '<body data-page="Грузоперевозки">\n' + sprite + "\n" + header("perevozki") + '<main id="top">\n'
pv += hero("Грузоперевозки",
           'Газель к подъезду<br>через <span class="y">30 минут.</span>',
           "Газели 4 и 6 метров по Ижевску, Удмуртии и межгороду.<br>От 1500 ₽ в час.",
           "#calc", "Рассчитать стоимость", "Цену называем до начала работ")
pv += trust()
pv += calc_section("perevozki", "Сколько стоит ваша перевозка?",
                   "Несколько вопросов, и вы увидите цену. Точную сумму подтвердим по телефону.")
pv += services("Услуги", "Перевезём что угодно.", [
    ("home", "Квартирный переезд", "Разберём мебель, упакуем, погрузим и расставим по комнатам на новом месте.", "от 1500 ₽/ч", "квартирный переезд"),
    ("office", "Офисный переезд", "Перевезём офис в выходные или вечером, чтобы работа не встала.", "от 1500 ₽/ч", "офисный переезд"),
    ("box", "Мебель и техника", "Диван, шкаф, холодильник, стиральная машина. Из магазина или между квартирами.", "от 1500 ₽/ч", "мебель и техника"),
    ("tool", "Стройматериалы", "Гипсокартон, профиль, мешки, плитка. С подъёмом на этаж грузчиками.", "от 1500 ₽/ч", "стройматериалы"),
    ("pin", "Межгород", "Воткинск, Сарапул, Можга, Глазов и дальше по России.", "по договорённости", "межгород"),
    ("evac", "Эвакуатор", "Эвакуация легковых автомобилей по Ижевску и пригороду.", "от 2500 ₽", "эвакуатор"),
], "")
pv += ptable([
    ("Газель 4 м", "квартира 1–2 комнаты, мебель, техника", "от 1500 ₽/ч"),
    ("Газель 6 м", "квартира 3+ комнат, дом, офис", "от 1500 ₽/ч"),
    ("Грузчик", "погрузка, разгрузка, подъём на этаж", "от 700 ₽/ч"),
    ("Эвакуатор", "по Ижевску", "от 2500 ₽"),
    ("Межгород", "Удмуртия и Россия", "по договорённости"),
], 'Не знаете, что выбрать? <a href="#" class="js-open" data-src="Цены: помочь с выбором">Оставьте заявку</a>, подберём самый выгодный вариант.', "alt")
pv += about() + pains()
pv += faq(FAQ_COMMON + [
    ("Какую газель выбрать?", "Газели 4 м хватает для переезда 1–2-комнатной квартиры или перевозки мебели. Газель 6 м берут для 3-комнатных квартир, домов и офисов. Сомневаетесь? Позвоните, подскажем."),
    ("Водитель помогает грузить?", "Водитель помогает с погрузкой и крепит груз. Для тяжёлой мебели и подъёма на этаж лучше заказать грузчиков, это можно отметить в калькуляторе."),
    ("Возите за город и в другие города?", "Да, по Удмуртии и России. Стоимость межгорода считаем индивидуально, позвоните или оставьте заявку."),
])
pv += contacts("Грузоперевозки", "Газель с водителем")
pv += "</main>\n" + tail(True)
(OUT / "perevozki.html").write_text(pv)

# ============================ Грузчики ============================
gr = head("Грузчики в Ижевске от 700 ₽/час · подача от 30 минут · Денис Ларин",
          "Грузчики и разнорабочие в Ижевске: погрузка, разгрузка, переезды, подъём стройматериалов, такелаж. От 700 ₽/час, подача от 30 минут. Рассчитайте стоимость онлайн.")
gr += '<body data-page="Грузчики">\n' + sprite + "\n" + header("gruzchiki") + '<main id="top">\n'
gr += hero("Грузчики и разнорабочие",
           'Грузчики в Ижевске.<br><span class="y">От 700 ₽ в час.</span>',
           "Погрузка, разгрузка, переезды, такелаж и подсобные работы.<br>Приезжаем от 30 минут.",
           "#calc", "Рассчитать стоимость", "Свои грузчики, без случайных людей")
gr += trust()
gr += calc_section("gruzchiki", "Сколько стоят грузчики?",
                   "Выберите работу, число людей и часы, и сразу увидите цену. Точную сумму подтвердим по телефону.")
gr += services("Услуги", "Работа для крепких рук.", [
    ("box", "Погрузка и разгрузка", "Машины, фуры, контейнеры. Быстро и аккуратно, с ремнями и тележками.", "от 700 ₽/ч", "погрузка/разгрузка"),
    ("home", "Помощь при переезде", "Вынесем, погрузим, поднимем на этаж и расставим по комнатам.", "от 700 ₽/ч", "переезд"),
    ("tool", "Подъём стройматериалов", "Гипсокартон, мешки, плитка, двери. На любой этаж, с лифтом и без.", "от 700 ₽/ч", "стройматериалы"),
    ("piano", "Такелаж", "Пианино, сейфы, станки и другие тяжёлые грузы. Ремни и опытная бригада.", "по договорённости", "такелаж"),
    ("trash", "Вынос мусора и мебели", "Строительный мусор, старые диваны и шкафы, хлам с балкона и гаража.", "от 700 ₽/ч", "вынос мусора"),
    ("people", "Разнорабочие", "Демонтаж, уборка, подсобные работы на стройке и даче.", "от 700 ₽/ч", "разнорабочие"),
], "")
gr += ptable([
    ("Грузчик", "погрузка, разгрузка, переезды", "от 700 ₽/ч"),
    ("Разнорабочий", "демонтаж, уборка, подсобные работы", "от 700 ₽/ч"),
    ("Газель с водителем", "4 или 6 метров, если нужна машина", "от 1500 ₽/ч"),
], 'Нужно много людей или работа на несколько дней? <a href="#" class="js-open" data-src="Цены: большой объём">Оставьте заявку</a>, посчитаем индивидуально.', "alt")
gr += pains() + about()
gr += faq(FAQ_COMMON + [
    ("Сколько грузчиков нужно?", "Для однокомнатной квартиры обычно хватает двух человек, для фуры или большого переезда нужно 3–4. Подскажем по телефону."),
    ("Грузчики трезвые?", "Да. Работаем своей бригадой, случайных людей не отправляем."),
    ("Можно заказать грузчиков без машины?", "Да, грузчиков можно заказать отдельно. А если понадобится газель, её тоже можно добавить в калькуляторе."),
])
gr += contacts("Грузчики", "Грузчики")
gr += "</main>\n" + tail(True)
(OUT / "gruzchiki.html").write_text(gr)

# ============================ Мини-приложение для Telegram ============================
mini = head("Расчёт стоимости · Переезды по Ижевску", "Калькулятор стоимости грузоперевозки и грузчиков.",
            '<script src="https://telegram.org/js/telegram-web-app.js"></script>\n<meta name="robots" content="noindex">\n')
mini += '<body class="miniapp" data-page="Telegram">\n' + sprite + """
<main>
  <div class="wiz" id="wiz" aria-live="polite"></div>
</main>
<script>
  // calc.html?type=gruzchiki — калькулятор грузчиков, иначе — грузоперевозки
  document.getElementById("wiz").dataset.wizard =
    new URLSearchParams(location.search).get("type") === "gruzchiki" ? "gruzchiki" : "perevozki";
</script>
<script src="assets/config.js"></script>
<script src="assets/site.js"></script>
<script src="assets/wizard.js"></script>
</body>
</html>
"""
(OUT / "calc.html").write_text(mini)
print("built")
