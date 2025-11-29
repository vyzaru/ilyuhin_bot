// Инициализация Telegram Web App
let tg = window.Telegram.WebApp;
let score = 0;
let gameActive = false;

// Расширяем на весь экран
tg.expand();

// Получаем данные пользователя
const user = tg.initDataUnsafe.user;

// Отображаем информацию о пользователе
if (user) {
    document.getElementById('user-data').innerHTML = `
        <p><strong>ID:</strong> ${user.id}</p>
        <p><strong>Имя:</strong> ${user.first_name}</p>
        <p><strong>Username:</strong> ${user.username || 'Не указан'}</p>
        <p><strong>Язык:</strong> ${user.language_code || 'Не указан'}</p>
    `;
} else {
    document.getElementById('user-data').innerHTML = '<p>Данные пользователя недоступны</p>';
}

// Функция отправки данных в бота
function sendData() {
    const data = {
        action: 'button_click',
        timestamp: new Date().toISOString(),
        user_id: user?.id,
        score: score
    };
    
    tg.sendData(JSON.stringify(data));
    tg.showPopup({
        title: 'Успешно!',
        message: 'Данные отправлены в бота',
        buttons: [{ type: 'ok' }]
    });
}

// Функция показа уведомления
function showAlert() {
    tg.showAlert('Привет из мини-приложения! 🎉');
}

// Функция смены темы
function changeTheme() {
    const currentTheme = tg.colorScheme;
    tg.setHeaderColor(currentTheme === 'dark' ? '#ffffff' : '#000000');
    tg.showPopup({
        title: 'Тема изменена',
        message: `Текущая тема: ${currentTheme}`,
        buttons: [{ type: 'ok' }]
    });
}

// Функции калькулятора
function calculate(operator) {
    const num1 = parseFloat(document.getElementById('num1').value) || 0;
    const num2 = parseFloat(document.getElementById('num2').value) || 0;
    let result;

    switch(operator) {
        case '+': result = num1 + num2; break;
        case '-': result = num1 - num2; break;
        case '*': result = num1 * num2; break;
        case '/': result = num2 !== 0 ? num1 / num2 : 'Ошибка: деление на 0'; break;
        default: result = 'Неизвестная операция';
    }

    document.getElementById('result').textContent = `Результат: ${result}`;
}

// Функции игры
function incrementScore() {
    if (gameActive) {
        score++;
        document.getElementById('score').textContent = score;
    }
}

function startGame() {
    score = 0;
    gameActive = true;
    document.getElementById('score').textContent = score;
    document.getElementById('game-btn').style.backgroundColor = '#dc3545';
    
    setTimeout(() => {
        gameActive = false;
        document.getElementById('game-btn').style.backgroundColor = '#2481cc';
        tg.showPopup({
            title: 'Игра окончена!',
            message: `Ваш счет: ${score}`,
            buttons: [{ type: 'ok' }]
        });
    }, 5000);
}

// Обработчик закрытия приложения
tg.onEvent('viewportChanged', () => {
    console.log('Viewport changed');
});

// Показываем основную кнопку
tg.MainButton.setText('Готово').show();
tg.MainButton.onClick(() => {
    tg.close();
});