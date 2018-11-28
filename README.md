# Генерация инфографики распределения госсредств на НКО

[Презентация проекта](https://github.com/farhit1/nonprofit-organizations-infographics/blob/master/about.pdf)

### Инструкция по запуску

1. Загрузить репозиторий `git clone https://github.com/farhit1/nonprofit-organizations-infographics`
2. Установить шрифты из папки `fonts`
3. Скачать данные и сделать предподсчет `python3 precalc.py`
4. [Получить api-key для telegram-бота](https://telegram.me/BotFather) и прописать его в `telegram/api_key.py`:
```python
API_KEY = '000000000:XXXXXXXXXXXXX_YYYYYYY_ZZZZZZZZZZZZZ'
```
5. Запустить бота `python3 main.py`

### Примеры получаемых изображений

![sample1](https://github.com/farhit1/nonprofit-organizations-infographics/blob/master/sample_results/sample1.jpg)
![sample3](https://github.com/farhit1/nonprofit-organizations-infographics/blob/master/sample_results/sample3.jpg)

### Требования

Python 3, Keynote
