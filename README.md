# Генерация инфографики распределения госсредств на НКО

Презентация проекта в `about.pdf`.

### Инструкция по запуску

0. Загрузить репозиторий `git clone https://github.com/farhit1/nonprofit-organizations-infographics`.
1. Скачать данные и сделать предподсчет `python3 precalc.py`
2. [Получить api-key для telegram-бота](https://telegram.me/BotFather) и прописать его в `telegram/api_key.py`:
```python
API_KEY = '000000000:XXXXXXXXXXXXX_YYYYYYY_ZZZZZZZZZZZZZ'
```
3. Запустить бота `python3 main.py`

### Примеры получаемых изображений

Примеры получаемых изображений лежат в `sample_results`.

### Требования

Python 3, Keynote