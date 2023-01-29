# chatGPT-telegram

## Ref

- <https://blog.stevenyu.tw/2022/12/04/利用-openai-gpt-3-寫一個-telegram-聊天機器人-cloudflare-tunnel-gcp-appengine/>
- <https://render.com>

## Setting

- Render Environment Variables
  - PYTHON_VERSION: 3.9.12
  - OPENAI_KEY
  - TELEGRAM_TOKEN
- `curl -L "https://api.telegram.org/bot{API_TOKEN}/setWebhook?url={RENDER_WEBSERVICE_ENDPOINT}/hook"`
