// Инициализация Telegram Web App
const tg = window.Telegram.WebApp;

// Расширяем на весь экран
tg.expand();

// Ждем загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('WebApp loaded');
    
    // Простая кнопка
    const button = document.createElement('button');
    button.textContent = '🎨 Отправить тест';
    button.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        right: 20px;
        padding: 16px;
        background: #0088cc;
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
    `;
    
    button.onclick = function() {
        console.log('Кнопка нажата');
        
        // Отправляем тестовые данные
        const testData = {
            action: "test",
            message: "Привет от Web App!",
            timestamp: Date.now()
        };
        
        tg.sendData(JSON.stringify(testData));
        console.log('Данные отправлены');
        
        // Закрываем
        setTimeout(() => tg.close(), 500);
    };
    
    document.body.appendChild(button);
    
    // Добавим простой текст
    const text = document.createElement('h1');
    text.textContent = 'Тестовое Mini App';
    text.style.cssText = 'color: white; text-align: center; margin-top: 50px;';
    document.body.appendChild(text);
});

// Фон для красоты
document.body.style.cssText = `
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    margin: 0;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
`;
