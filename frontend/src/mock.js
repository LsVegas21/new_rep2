// Mock data for landing page generator
export const mockGeneratedLandings = [
  {
    id: '1',
    theme: 'Фитнес-тренировки онлайн',
    language: 'Русский',
    trafficSource: 'Google Ads',
    targetAction: 'Регистрация на пробное занятие',
    createdAt: new Date().toISOString(),
    html: `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Онлайн Фитнес - Первая тренировка бесплатно</title>
</head>
<body>
    <h1>Трансформируйте своё тело за 30 дней</h1>
    <p>Персональные тренировки с профессиональным тренером онлайн</p>
    <button>Начать бесплатно</button>
</body>
</html>`,
    lighthouse: 98
  }
];

export const mockThemes = [
  'E-commerce',
  'SaaS продукт',
  'Образовательные курсы',
  'Фитнес и здоровье',
  'Недвижимость',
  'Финансовые услуги',
  'Юридические услуги',
  'Медицинские услуги'
];

export const mockLanguages = [
  'Русский',
  'English',
  'Español',
  'Deutsch',
  'Français',
  'Italiano',
  'Português',
  '中文',
  '日本語'
];

export const mockTrafficSources = [
  'Google Ads',
  'Facebook Ads',
  'Instagram Ads',
  'TikTok Ads',
  'LinkedIn Ads',
  'YouTube Ads',
  'Yandex Direct',
  'VK Ads'
];

export const mockTargetActions = [
  'Заказать звонок',
  'Оставить заявку',
  'Купить сейчас',
  'Зарегистрироваться',
  'Скачать',
  'Получить консультацию',
  'Записаться на демо',
  'Подписаться'
];