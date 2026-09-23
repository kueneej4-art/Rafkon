# Сайт «Переезды по Ижевску» · Денис Ларин

Продающий сайт под Яндекс.Директ в стиле Apple. Каждая заявка сразу приходит в
Telegram вместе с расчётом из калькулятора и меткой, из какой рекламы пришёл клиент.

## Страницы

| Страница | Для чего | Куда вести рекламу |
|---|---|---|
| `index.html` | главная: цены, выбор услуги, эвакуатор | общие запросы, «переезд ижевск» |
| `perevozki.html` | **грузоперевозки** + калькулятор перевозки | «газель», «грузоперевозки» |
| `gruzchiki.html` | **грузчики** + калькулятор грузчиков | «грузчики», «разнорабочие» |
| `calc.html?type=perevozki` / `?type=gruzchiki` | только калькулятор: для кнопки в Telegram-боте (Mini App) | — |
| `privacy.html` | политика конфиденциальности (152-ФЗ) | — |

## Где что менять

- **`assets/config.js`**: телефоны, WhatsApp, Telegram, ВКонтакте, адрес, номер Метрики
  и **все цены калькуляторов**. Это главный файл настроек.
- `assets/wizard.js`: вопросы калькуляторов.
- `assets/style.css`: дизайн.
- Тексты страниц собираются скриптом: правьте `_build/build.py` и запускайте
  `python3 _build/build.py`. Если править `*.html` вручную, следующий запуск скрипта
  перезапишет эти правки.

## Как запустить (≈15 минут)

1. **Netlify → Add new site → Import from GitHub** → репозиторий `Rafkon`,
   **Base directory** = `gruzchiki`.
2. **Site configuration → Environment variables**:
   - `TELEGRAM_BOT_TOKEN`: токен бота от @BotFather;
   - `TELEGRAM_CHAT_ID`: необязательно, по умолчанию заявки идут на ID 275264199
     (несколько через запятую). Боту нужно хоть раз написать `/start`.
3. **Deploy**, затем отправьте тестовую заявку: она должна прийти в Telegram.
4. Подключите домен (Domain management), HTTPS Netlify выдаст сам.

## Telegram-бот с калькулятором (без отдельного сервера)

Кнопки «Заявка в Telegram» на сайте открывают калькулятор прямо внутри бота.
Пока бот не указан, они ведут в личный Telegram (`telegram` в `config.js`).

1. @BotFather → `/newbot` → имя и username (например `larin_pereezdy_bot`).
   Этот же токен впишите в Netlify как `TELEGRAM_BOT_TOKEN`: заявки будут приходить от этого бота.
2. @BotFather → `/mybots` → ваш бот → **Bot Settings → Configure Mini App → Enable Mini App**
   → ссылка `https://ваш-сайт.netlify.app/calc.html`.
3. Там же **Menu Button** → та же ссылка, текст кнопки «Рассчитать».
4. **Edit Description**: «Рассчитаем стоимость перевозки и грузчиков за минуту. Нажмите «Рассчитать».»
5. В `assets/config.js` впишите `bot: "larin_pereezdy_bot"` (без @).

Ссылки вида `t.me/<бот>?startapp=perevozki` и `?startapp=gruzchiki` сразу открывают нужный
калькулятор. Заявка из бота приходит вам так же, как с сайта, вместе с ником клиента.

## Яндекс.Метрика (обязательно для Директа)

1. Создайте счётчик на metrika.yandex.ru, включите Вебвизор, впишите номер в `metrikaId`.
2. Цели → **JavaScript-событие**:

| Идентификатор | Когда срабатывает |
|---|---|
| `lead` | заявка отправлена (**главная цель для Директа**) |
| `phone_click` | клик по телефону |
| `messenger_click` | клик по WhatsApp / Telegram / ВКонтакте |
| `calc_start` | начали пользоваться калькулятором |
| `form_open` | открыли всплывающую форму |

Составная цель «Все обращения» = `lead` + `phone_click` + `messenger_click`.

## UTM-метки для объявлений

```
?utm_source=yandex&utm_medium=cpc&utm_campaign={campaign_id}&utm_content={ad_id}&utm_term={keyword}
```
