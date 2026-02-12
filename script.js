// Инициализация Telegram Web App
const tg = window.Telegram.WebApp;

// Расширяем на весь экран
tg.expand();

// Настройка кнопки Telegram
tg.MainButton.setText("🎨 Создать тему").show();

// Элементы DOM
const themeName = document.getElementById("themeName");
const bgColor = document.getElementById("bgColor");
const accentColor = document.getElementById("accentColor");
const textColor = document.getElementById("textColor");
const bgHex = document.getElementById("bgHex");
const accentHex = document.getElementById("accentHex");
const textHex = document.getElementById("textHex");
const themePreview = document.getElementById("themePreview");
const togglePreview = document.getElementById("togglePreview");
const generateBtn = document.getElementById("generateBtn");
const randomBtn = document.getElementById("randomBtn");

// Цветовые палитры для случайных тем
const colorPalettes = [
  { bg: "#1a1a1a", accent: "#0088cc", text: "#ffffff" },
  { bg: "#0f0f23", accent: "#ff6b6b", text: "#ffffff" },
  { bg: "#2d3436", accent: "#00b894", text: "#ffffff" },
  { bg: "#ffffff", accent: "#0984e3", text: "#2d3436" },
  { bg: "#f8f9fa", accent: "#e84393", text: "#2d3436" },
  { bg: "#1e3799", accent: "#f6b93b", text: "#ffffff" },
  { bg: "#2c2c54", accent: "#33d9b2", text: "#ffffff" },
  { bg: "#182C61", accent: "#FC427B", text: "#ffffff" },
];

// Обновление HEX значений
function updateHexValues() {
  bgHex.textContent = bgColor.value;
  accentHex.textContent = accentColor.value;
  textHex.textContent = textColor.value;
}

// Обновление превью темы
function updateThemePreview() {
  document.documentElement.style.setProperty("--bg", bgColor.value);
  document.documentElement.style.setProperty("--accent", accentColor.value);
  document.documentElement.style.setProperty("--text", textColor.value);
}

// Показ/скрытие превью
togglePreview.addEventListener("click", function () {
  themePreview.classList.toggle("show");
  togglePreview.textContent = themePreview.classList.contains("show")
    ? "👁️ Скрыть превью"
    : "👁️ Показать превью";
});

// Генерация случайной темы
randomBtn.addEventListener("click", function () {
  const randomPalette =
    colorPalettes[Math.floor(Math.random() * colorPalettes.length)];

  bgColor.value = randomPalette.bg;
  accentColor.value = randomPalette.accent;
  textColor.value = randomPalette.text;

  updateHexValues();
  updateThemePreview();

  // Анимация кнопки
  randomBtn.style.transform = "scale(0.95)";
  setTimeout(() => {
    randomBtn.style.transform = "scale(1)";
  }, 150);
});

// Создание темы
generateBtn.addEventListener("click", function () {
  const theme = {
    name: themeName.value || "Моя тема",
    dominant: bgColor.value,
    accent: accentColor.value,
    text: textColor.value,
    is_dark: isDarkColor(bgColor.value),
  };

  // Отправка данных в бота через Telegram Web App
  tg.sendData(
    JSON.stringify({
      action: "apply_theme",
      theme: theme,
    })
  );

  // Показываем уведомление
  tg.showAlert("🎨 Тема создана! Возвращайтесь в бота для установки.");

  // Анимация кнопки
  generateBtn.style.transform = "scale(0.95)";
  setTimeout(() => {
    generateBtn.style.transform = "scale(1)";
  }, 150);
});

// Определение темный ли цвет
function isDarkColor(hex) {
  hex = hex.replace("#", "");
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);

  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness < 128;
}

// Слушатели изменений
bgColor.addEventListener("input", function () {
  updateHexValues();
  updateThemePreview();
});

accentColor.addEventListener("input", function () {
  updateHexValues();
  updateThemePreview();
});

textColor.addEventListener("input", function () {
  updateHexValues();
  updateThemePreview();
});

// Инициализация
updateHexValues();
updateThemePreview();

// Показываем превью
themePreview.classList.add("show");
togglePreview.textContent = "👁️ Скрыть превью";
