# -*- coding: utf-8 -*-
"""
打飞机游戏 - 关卡配置文件
定义8个关卡和8种敌机类型的配置
"""

# 敌机类型配置
ENEMY_TYPES = {
    1: {
        'name': '侦察机',
        'image': 'plane_models/plane_1.png',
        'hp': 1,
        'speed': 2.0,
        'shoot_probability': 0.005,
        'score': 10
    },
    2: {
        'name': '轻型战机',
        'image': 'plane_models/plane_2.png',
        'hp': 2,
        'speed': 2.5,
        'shoot_probability': 0.008,
        'score': 15
    },
    3: {
        'name': '重型战机',
        'image': 'plane_models/plane_3.png',
        'hp': 3,
        'speed': 1.8,
        'shoot_probability': 0.010,
        'score': 20
    },
    4: {
        'name': '喷气战机',
        'image': 'plane_models/plane_4.png',
        'hp': 2,
        'speed': 3.5,
        'shoot_probability': 0.012,
        'score': 25
    },
    5: {
        'name': '轰炸机',
        'image': 'plane_models/plane_5.png',
        'hp': 5,
        'speed': 1.5,
        'shoot_probability': 0.015,
        'score': 30
    },
    6: {
        'name': '隐形战机',
        'image': 'plane_models/plane_6.png',
        'hp': 3,
        'speed': 4.0,
        'shoot_probability': 0.010,
        'score': 35
    },
    7: {
        'name': '精英战机',
        'image': 'plane_models/plane_7.png',
        'hp': 4,
        'speed': 3.0,
        'shoot_probability': 0.018,
        'score': 40
    },
    8: {
        'name': 'BOSS',
        'image': 'plane_models/plane_8.png',
        'hp': 10,
        'speed': 2.0,
        'shoot_probability': 0.025,
        'score': 100
    }
}

# 关卡配置
LEVELS = [
    {
        'level': 1,
        'name': '新手训练',
        'enemy_types': [1],
        'spawn_interval': 80,
        'kills_required': 3,
        'description': '基础训练'
    },
    {
        'level': 2,
        'name': '空中巡逻',
        'enemy_types': [1, 2],
        'spawn_interval': 70,
        'kills_required': 3,
        'description': '混合敌机'
    },
    {
        'level': 3,
        'name': '激烈对抗',
        'enemy_types': [2, 3],
        'spawn_interval': 60,
        'kills_required': 3,
        'description': '生命值提升'
    },
    {
        'level': 4,
        'name': '高速追击',
        'enemy_types': [2, 3, 4],
        'spawn_interval': 55,
        'kills_required': 3,
        'description': '高速敌机'
    },
    {
        'level': 5,
        'name': '轰炸突袭',
        'enemy_types': [3, 4, 5],
        'spawn_interval': 50,
        'kills_required': 3,
        'description': '高HP轰炸机'
    },
    {
        'level': 6,
        'name': '隐形威胁',
        'enemy_types': [4, 5, 6],
        'spawn_interval': 45,
        'kills_required': 3,
        'description': '超高速'
    },
    {
        'level': 7,
        'name': '精英部队',
        'enemy_types': [5, 6, 7],
        'spawn_interval': 40,
        'kills_required': 3,
        'description': '密集射击'
    },
    {
        'level': 8,
        'name': '最终决战',
        'enemy_types': [6, 7, 8],
        'spawn_interval': 50,
        'kills_required': 3,
        'description': '终极挑战'
    }
]
