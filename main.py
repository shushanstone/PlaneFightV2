# -*- coding: utf-8 -*-
"""
打飞机小游戏
技术栈: Python 3 + Pygame
平台: macOS
"""

import pygame
import random
import sys
import os
from level_config import ENEMY_TYPES, LEVELS

# 初始化Pygame
pygame.init()
pygame.mixer.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 玩家属性
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_BULLET_SPEED = 4
SHOOT_COOLDOWN = 200  # 毫秒

# 字体加载 - 支持中文
def load_font(size):
    """加载支持中文的字体"""
    font_paths = [
        '/System/Library/Fonts/Hiragino Sans GB.ttc',  # 苹方黑体
        '/System/Library/Fonts/STHeiti Medium.ttc',     # 华文黑体
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue
    
    # 如果都失败，使用默认字体
    return pygame.font.Font(None, size)

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load('assets/player.png').convert_alpha()
        except:
            # 如果加载失败，创建一个简单的矩形
            self.image = pygame.Surface((60, 80))
            self.image.fill((74, 144, 226))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.last_shot = 0
        
    def update(self):
        # 获取按键
        keys = pygame.key.get_pressed()
        
        # 移动控制
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
            
    def shoot(self):
        """发射子弹"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > SHOOT_COOLDOWN:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            return bullet
        return None

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        config = ENEMY_TYPES[enemy_type]
        
        # 加载敌机图片
        try:
            self.image = pygame.image.load(config['image']).convert_alpha()
        except:
            # 如果加载失败，创建一个简单的矩形
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        
        # 敌机属性
        self.hp = config['hp']
        self.max_hp = config['hp']
        self.speed = config['speed']
        self.shoot_probability = config['shoot_probability']
        self.score = config['score']
        self.name = config['name']
        
    def update(self):
        self.rect.y += self.speed
        
        # 如果敌机离开屏幕，则删除
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
    def shoot(self):
        """敌机射击"""
        if random.random() < self.shoot_probability:
            return EnemyBullet(self.rect.centerx, self.rect.bottom)
        return None
        
    def hit(self):
        """敌机受到伤害"""
        self.hp -= 1
        if self.hp <= 0:
            return True
        return False

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load('assets/bullet.png').convert_alpha()
        except:
            self.image = pygame.Surface((8, 20))
            self.image.fill((241, 196, 15))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED
        
    def update(self):
        self.rect.y -= self.speed
        
        # 如果子弹离开屏幕，则删除
        if self.rect.bottom < 0:
            self.kill()

# 敌机子弹类
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load('assets/enemy_bullet.png').convert_alpha()
        except:
            self.image = pygame.Surface((6, 15))
            self.image.fill((231, 76, 60))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = ENEMY_BULLET_SPEED
        
    def update(self):
        self.rect.y += self.speed
        
        # 如果子弹离开屏幕，则删除
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# 爆炸效果类
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load('assets/explosion.png').convert_alpha()
        except:
            self.image = pygame.Surface((64, 64))
            self.image.fill((255, 165, 0))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.frame_rate = 3
        self.last_update = pygame.time.get_ticks()
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate * 10:
            self.frame += 1
            if self.frame > 8:
                self.kill()
            else:
                self.last_update = now

# 关卡管理器
class LevelManager:
    def __init__(self):
        self.current_level = 0
        self.kills_in_level = 0
        self.transition_timer = 0
        self.in_transition = False
        
    def get_current_level(self):
        """获取当前关卡配置"""
        if self.current_level < len(LEVELS):
            return LEVELS[self.current_level]
        return None
        
    def enemy_killed(self):
        """敌机被击败"""
        self.kills_in_level += 1
        level = self.get_current_level()
        
        if level and self.kills_in_level >= level['kills_required']:
            # 通关当前关卡
            self.in_transition = True
            self.transition_timer = 120  # 2秒过渡时间 (60fps * 2)
            
    def update(self):
        """更新关卡状态"""
        if self.in_transition:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                self.current_level += 1
                self.kills_in_level = 0
                self.in_transition = False
                
    def is_game_complete(self):
        """检查是否通关所有关卡"""
        return self.current_level >= len(LEVELS)
        
    def get_progress(self):
        """获取当前关卡进度"""
        level = self.get_current_level()
        if level:
            return self.kills_in_level, level['kills_required']
        return 0, 0

# 游戏主类
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('打飞机小游戏')
        self.clock = pygame.time.Clock()
        
        # 加载字体
        self.font = load_font(36)
        self.small_font = load_font(24)
        
        # 加载背景
        try:
            self.background = pygame.image.load('assets/background.png').convert()
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((10, 14, 39))
        
        # 加载音效
        self.load_sounds()
        
        # 精灵组
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        
        # 创建玩家
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # 游戏状态
        self.score = 0
        self.game_over = False
        self.enemy_spawn_timer = 0
        
        # 关卡管理器
        self.level_manager = LevelManager()
        
        # 播放背景音乐
        if self.bg_music:
            self.bg_music.play(-1)
            
    def load_sounds(self):
        """加载音效"""
        self.sounds = {}
        try:
            self.sounds['shoot'] = pygame.mixer.Sound('assets/shoot.wav')
            self.sounds['shoot'].set_volume(0.3)
        except:
            self.sounds['shoot'] = None
            
        try:
            self.sounds['explosion'] = pygame.mixer.Sound('assets/explosion.wav')
            self.sounds['explosion'].set_volume(0.5)
        except:
            self.sounds['explosion'] = None
            
        try:
            self.sounds['game_over'] = pygame.mixer.Sound('assets/game_over.wav')
            self.sounds['game_over'].set_volume(0.6)
        except:
            self.sounds['game_over'] = None
            
        try:
            self.bg_music = pygame.mixer.Sound('assets/background.wav')
            self.bg_music.set_volume(0.3)
        except:
            self.bg_music = None
            
    def spawn_enemy(self):
        """生成敌机"""
        level = self.level_manager.get_current_level()
        if level:
            enemy_type = random.choice(level['enemy_types'])
            enemy = Enemy(enemy_type)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
            
    def run(self):
        """游戏主循环"""
        running = True
        while running:
            self.clock.tick(FPS)
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        bullet = self.player.shoot()
                        if bullet:
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)
                            if self.sounds['shoot']:
                                self.sounds['shoot'].play()
                    elif event.key == pygame.K_r and self.game_over:
                        self.__init__()  # 重新开始
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # 更新游戏
            if not self.game_over and not self.level_manager.in_transition:
                self.update()
            
            # 更新关卡状态
            self.level_manager.update()
            
            # 渲染
            self.draw()
            
        pygame.quit()
        sys.exit()
        
    def update(self):
        """更新游戏状态"""
        # 检查是否通关所有关卡
        if self.level_manager.is_game_complete():
            return
            
        # 更新所有精灵
        self.all_sprites.update()
        
        # 生成敌机
        level = self.level_manager.get_current_level()
        if level:
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= level['spawn_interval']:
                self.spawn_enemy()
                self.enemy_spawn_timer = 0
        
        # 敌机射击
        for enemy in self.enemies:
            enemy_bullet = enemy.shoot()
            if enemy_bullet:
                self.all_sprites.add(enemy_bullet)
                self.enemy_bullets.add(enemy_bullet)
        
        # 检测玩家子弹与敌机的碰撞
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy in hits:
            if enemy.hit():
                # 敌机被摧毁
                self.score += enemy.score
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.all_sprites.add(explosion)
                self.explosions.add(explosion)
                enemy.kill()
                
                if self.sounds['explosion']:
                    self.sounds['explosion'].play()
                    
                # 更新关卡进度
                self.level_manager.enemy_killed()
        
        # 检测敌机子弹与玩家的碰撞
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if hits:
            self.player.lives -= 1
            explosion = Explosion(self.player.rect.centerx, self.player.rect.centery)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            
            if self.sounds['explosion']:
                self.sounds['explosion'].play()
                
            if self.player.lives <= 0:
                self.game_over = True
                if self.bg_music:
                    self.bg_music.stop()
                if self.sounds['game_over']:
                    self.sounds['game_over'].play()
        
        # 检测敌机与玩家的碰撞
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hits:
            self.player.lives -= 1
            for enemy in hits:
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.all_sprites.add(explosion)
                self.explosions.add(explosion)
                
            if self.sounds['explosion']:
                self.sounds['explosion'].play()
                
            if self.player.lives <= 0:
                self.game_over = True
                if self.bg_music:
                    self.bg_music.stop()
                if self.sounds['game_over']:
                    self.sounds['game_over'].play()
    
    def draw(self):
        """渲染游戏画面"""
        # 绘制背景
        self.screen.blit(self.background, (0, 0))
        
        # 绘制所有精灵
        self.all_sprites.draw(self.screen)
        
        # 绘制UI
        self.draw_ui()
        
        # 绘制关卡过渡动画
        if self.level_manager.in_transition:
            self.draw_level_transition()
        
        # 绘制游戏结束或通关画面
        if self.game_over:
            self.draw_game_over()
        elif self.level_manager.is_game_complete():
            self.draw_victory()
        
        pygame.display.flip()
        
    def draw_ui(self):
        """绘制游戏UI"""
        # 绘制分数
        score_text = self.small_font.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 绘制生命值
        lives_text = self.small_font.render(f'生命: {self.player.lives}', True, WHITE)
        self.screen.blit(lives_text, (10, 40))
        
        # 绘制关卡信息
        level = self.level_manager.get_current_level()
        if level:
            level_text = self.small_font.render(
                f'关卡 {level["level"]}: {level["name"]}', 
                True, WHITE
            )
            self.screen.blit(level_text, (SCREEN_WIDTH - 250, 10))
            
            # 绘制进度
            current, required = self.level_manager.get_progress()
            progress_text = self.small_font.render(
                f'进度: {current}/{required}', 
                True, WHITE
            )
            self.screen.blit(progress_text, (SCREEN_WIDTH - 250, 40))
            
            # 绘制进度条
            bar_width = 200
            bar_height = 20
            bar_x = 10
            bar_y = 70
            
            # 背景
            pygame.draw.rect(self.screen, WHITE, 
                           (bar_x, bar_y, bar_width, bar_height), 2)
            
            # 进度
            if required > 0:
                progress_width = int(bar_width * current / required)
                pygame.draw.rect(self.screen, GREEN, 
                               (bar_x, bar_y, progress_width, bar_height))
    
    def draw_level_transition(self):
        """绘制关卡过渡动画"""
        # 半透明黑色遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # 关卡完成文本
        completed_text = self.font.render('关卡完成!', True, GREEN)
        text_rect = completed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(completed_text, text_rect)
        
        # 下一关信息
        next_level = self.level_manager.current_level + 1
        if next_level < len(LEVELS):
            next_level_info = LEVELS[next_level]
            next_text = self.small_font.render(
                f'准备进入关卡 {next_level_info["level"]}: {next_level_info["name"]}', 
                True, WHITE
            )
            text_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(next_text, text_rect)
    
    def draw_game_over(self):
        """绘制游戏结束画面"""
        # 半透明黑色遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文本
        game_over_text = self.font.render('游戏结束!', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # 最终分数
        score_text = self.small_font.render(f'最终分数: {self.score}', True, WHITE)
        text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, text_rect)
        
        # 重新开始提示
        restart_text = self.small_font.render('按 R 重新开始 | 按 ESC 退出', True, WHITE)
        text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, text_rect)
    
    def draw_victory(self):
        """绘制通关画面"""
        # 半透明黑色遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # 恭喜通关文本
        victory_text = self.font.render('恭喜通关!', True, GREEN)
        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(victory_text, text_rect)
        
        # 最终分数
        score_text = self.small_font.render(f'最终分数: {self.score}', True, WHITE)
        text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, text_rect)
        
        # 重新开始提示
        restart_text = self.small_font.render('按 R 重新开始 | 按 ESC 退出', True, WHITE)
        text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, text_rect)

# 主程序入口
if __name__ == '__main__':
    game = Game()
    game.run()
