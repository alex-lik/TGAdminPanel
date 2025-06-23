 Инструкция по установке и запуску проекта telegram-content-manager (Vite + React + TailwindCSS 4.x)
1. Клонирование репозитория
bash
Копировать
Редактировать
git clone <URL_ТВОЕГО_РЕПОЗИТОРИЯ>
cd telegram-content-manager
2. Структура проекта
plaintext
Копировать
Редактировать
telegram-content-manager/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   ├── index.css
│   └── ...
├── package.json
├── postcss.config.cjs
├── tailwind.config.js
├── tsconfig.json
├── docker-compose.yml
├── Dockerfile
├── ...
3. Правильная настройка TailwindCSS 4.x c PostCSS
3.1. Установи зависимости:
bash
Копировать
Редактировать
npm install
npm install @tailwindcss/postcss --save-dev
3.2. Проверь и поправь файл postcss.config.cjs:
js
Копировать
Редактировать
// postcss.config.cjs
module.exports = {
  plugins: [
    require('@tailwindcss/postcss')(),
    require('autoprefixer'),
  ],
};
Важно: Используется именно @tailwindcss/postcss!

3.3. Проверь файл tailwind.config.js (ESM или CommonJS):
js
Копировать
Редактировать
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: { extend: {} },
  plugins: [],
}
или, если ESM не поддерживается:

js
Копировать
Редактировать
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: { extend: {} },
  plugins: [],
}
4. Проверь структуру src/
В папке src/ должен лежать твой index.css с содержимым:

css
Копировать
Редактировать
@tailwind base;
@tailwind components;
@tailwind utilities;
/* свои стили... */
5. Docker-сборка (рекомендуется для prod)
5.1. Проверь, что нет лишних файлов-конфигов (только postcss.config.cjs)
bash
Копировать
Редактировать
ls postcss.config.*
Должен быть только postcss.config.cjs.

5.2. Собери и запусти контейнер:
bash
Копировать
Редактировать
docker-compose build frontend
docker-compose up frontend
6. Локальный запуск без Docker (dev-режим)
bash
Копировать
Редактировать
npm install
npm run dev
Откроется по адресу http://localhost:5173 (или другому, указанному Vite).

7. Тестирование production-сборки (локально)
bash
Копировать
Редактировать
npm run build
npm run preview
8. Частые ошибки и решения
Ошибка про PostCSS и Tailwind:
“The PostCSS plugin has moved to a separate package…”
→ Решение:

sql
Копировать
Редактировать
npm install @tailwindcss/postcss --save-dev
И поправь postcss.config.cjs как выше.

Ошибка “module is not defined in ES module scope” или “require is not defined”
→ Решение:
Переименуй конфиг в postcss.config.cjs и используй module.exports вместо export default.

Ошибка TypeScript “'React' is declared but its value is never read”
→ Решение:
Удали неиспользуемый импорт React из компонентов.

“Cannot find module './index.css'”
→ Решение:
Убедись, что index.css лежит в папке src, и импортируется как ./index.css.

9. Минимальный рабочий postcss.config.cjs для Tailwind 4.x
js
Копировать
Редактировать
module.exports = {
  plugins: [
    require('@tailwindcss/postcss')(),
    require('autoprefixer'),
  ],
};
10. Возможные дополнительные команды
Обновить npm до последней версии:

bash
Копировать
Редактировать
npm install -g npm
Если поменял конфиги — пересобирай контейнер полностью:

bash
Копировать
Редактировать
docker-compose build --no-cache frontend
docker-compose up frontend
Итого
Используй @tailwindcss/postcss с Tailwind 4.x и PostCSS!

Всегда следи за расположением файлов и типами модулей (.js для ESM, .cjs для CommonJS).

Если видишь ошибку в логе — смотри внимательно, что именно не нравится билд-системе, и читай стек-трейс.

