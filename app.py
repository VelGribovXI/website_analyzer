from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import random
import re
from collections import defaultdict

app = Flask(__name__)

# База данных для хранения статистики (в реальном проекте используйте БД)
# Здесь для демонстрации используем словарь
websites_stats = {}

def parse_user_agent(user_agent_string):
    """Определяет тип устройства по User-Agent"""
    user_agent_string = user_agent_string.lower()
    
    if 'mobile' in user_agent_string or 'android' in user_agent_string or 'iphone' in user_agent_string:
        return 'Мобильное устройство'
    elif 'tablet' in user_agent_string or 'ipad' in user_agent_string:
        return 'Планшет'
    else:
        return 'Компьютер'

def generate_demo_stats(website_url):
    """Генерирует демонстрационную статистику для веб-сайта"""
    # Создаем ключ для сайта
    site_key = website_url.lower().strip()
    
    if site_key not in websites_stats:
        # Генерируем случайные данные за последние 30 дней
        stats = {
            'daily_visits': [],
            'devices': {'Компьютер': 0, 'Мобильное устройство': 0, 'Планшет': 0},
            'total_visits': 0
        }
        
        today = datetime.now()
        for i in range(30):
            date = today - timedelta(days=29-i)
            # Генерируем случайное количество посещений от 50 до 500
            visits = random.randint(50, 500)
            stats['daily_visits'].append({
                'date': date.strftime('%Y-%m-%d'),
                'visits': visits
            })
            stats['total_visits'] += visits
        
        # Генерируем распределение по устройствам
        total = stats['total_visits']
        stats['devices']['Компьютер'] = int(total * random.uniform(0.4, 0.7))
        stats['devices']['Мобильное устройство'] = int(total * random.uniform(0.3, 0.5))
        stats['devices']['Планшет'] = total - stats['devices']['Компьютер'] - stats['devices']['Мобильное устройство']
        
        websites_stats[site_key] = stats
    
    return websites_stats[site_key]

def get_real_time_stats(website_url):
    """Получает реальную статистику (упрощенная версия)"""
    # В реальном проекте здесь был бы парсинг аналитики или API
    # Сейчас возвращаем демо-данные
    return generate_demo_stats(website_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    website_url = data.get('url', '')
    
    if not website_url:
        return jsonify({'error': 'Пожалуйста, введите URL сайта'}), 400
    
    # Добавляем http:// если нет протокола
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url
    
    # Получаем статистику
    stats = get_real_time_stats(website_url)
    
    # Получаем User-Agent для демонстрации (в реальном проекте брали бы из запроса)
    user_agent = request.headers.get('User-Agent', '')
    current_device = parse_user_agent(user_agent)
    
    return jsonify({
        'url': website_url,
        'total_visits': stats['total_visits'],
        'daily_stats': stats['daily_visits'],
        'devices': stats['devices'],
        'current_device': current_device
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
