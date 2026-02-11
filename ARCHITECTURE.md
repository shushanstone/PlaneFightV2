# 打飞机游戏 - 系统架构文档

## 📋 目录

- [系统概述](#系统概述)
- [架构设计](#架构设计)
- [核心模块](#核心模块)
- [数据流转](#数据流转)
- [时序图](#时序图)
- [设计模式](#设计模式)

---

## 系统概述

本游戏采用经典的**游戏循环架构**，基于Pygame框架实现。整体架构遵循**面向对象设计**原则，将游戏实体抽象为独立的类，通过Sprite组管理和更新。

### 核心特点

- **分层架构**: 配置层、实体层、管理层、渲染层
- **事件驱动**: 基于Pygame事件循环
- **组件化设计**: 使用Sprite Group管理游戏对象
- **配置分离**: 关卡和敌机配置独立于游戏逻辑

---

## 架构设计

### 1. 系统架构图

```mermaid
graph TB
    subgraph UserInterface["用户界面层"]
        GameWindow["游戏窗口<br/>800x600"]
        UI["UI渲染<br/>分数/生命/关卡"]
    end

    subgraph GameCore["游戏核心层"]
        GameLoop["游戏主循环<br/>60 FPS"]
        EventHandler["事件处理器<br/>键盘/退出"]
        CollisionDetector["碰撞检测器"]
        LevelMgr["关卡管理器<br/>LevelManager"]
    end

    subgraph EntityLayer["实体层"]
        Player["玩家 Player"]
        Enemy["敌机 Enemy"]
        Bullet["子弹 Bullet"]
        EnemyBullet["敌机子弹<br/>EnemyBullet"]
        Explosion["爆炸效果<br/>Explosion"]
    end

    subgraph ResourceLayer["资源层"]
        Images["图片资源<br/>assets/"]
        Sounds["音效资源<br/>WAV文件"]
        Config["关卡配置<br/>level_config.py"]
    end

    subgraph SpriteGroups["Sprite组管理"]
        AllSprites["all_sprites"]
        Enemies["enemies"]
        Bullets["bullets"]
        EnemyBullets["enemy_bullets"]
        Explosions["explosions"]
    end

    GameWindow --> GameLoop
    GameLoop --> EventHandler
    GameLoop --> LevelMgr
    GameLoop --> CollisionDetector
    GameLoop --> UI

    EventHandler --> Player
    
    LevelMgr --> Config
    LevelMgr --> Enemy
    
    CollisionDetector --> AllSprites
    
    Player --> SpriteGroups
    Enemy --> SpriteGroups
    Bullet --> SpriteGroups
    EnemyBullet --> SpriteGroups
    Explosion --> SpriteGroups
    
    Config --> Enemy
    Images --> EntityLayer
    Sounds --> GameLoop
```

### 2. 类图结构

```mermaid
classDiagram
    class Game {
        -screen: Surface
        -clock: Clock
        -player: Player
        -level_manager: LevelManager
        -score: int
        -game_over: bool
        +run()
        +update()
        +draw()
        +spawn_enemy()
    }

    class Player {
        -lives: int
        -speed: int
        -last_shot: int
        +update()
        +shoot() Bullet
    }

    class Enemy {
        -enemy_type: int
        -hp: int
        -speed: float
        -shoot_probability: float
        -score: int
        +update()
        +shoot() EnemyBullet
        +hit() bool
    }

    class Bullet {
        -speed: int
        +update()
    }

    class EnemyBullet {
        -speed: int
        +update()
    }

    class Explosion {
        -frame: int
        -frame_rate: int
        +update()
    }

    class LevelManager {
        -current_level: int
        -kills_in_level: int
        -in_transition: bool
        +get_current_level() dict
        +enemy_killed()
        +update()
        +is_game_complete() bool
    }

    class Sprite {
        <<pygame.sprite.Sprite>>
        +image: Surface
        +rect: Rect
        +update()
    }

    Sprite <|-- Player
    Sprite <|-- Enemy
    Sprite <|-- Bullet
    Sprite <|-- EnemyBullet
    Sprite <|-- Explosion

    Game --> Player
    Game --> Enemy
    Game --> LevelManager
    Game ..> Bullet
    Game ..> EnemyBullet
    Game ..> Explosion
```

---

## 核心模块

### 1. Game（游戏主类）

**职责**: 游戏的总控制器，管理游戏循环和所有子系统

**核心属性**:
- `screen`: 游戏窗口
- `player`: 玩家实例
- `level_manager`: 关卡管理器
- `all_sprites`: 所有游戏对象的集合
- 各种Sprite组（enemies, bullets等）

**核心方法**:
- `run()`: 主游戏循环
- `update()`: 更新游戏状态
- `draw()`: 渲染游戏画面
- `spawn_enemy()`: 生成敌机

### 2. LevelManager（关卡管理器）

**职责**: 管理关卡进度、切换和通关判定

**状态机**:
```
正常游戏 → 击败目标数 → 过渡状态 → 下一关 → 正常游戏
                                    ↓
                                  通关
```

**核心属性**:
- `current_level`: 当前关卡索引
- `kills_in_level`: 当前关卡击杀数
- `in_transition`: 是否在过渡动画中

**核心方法**:
- `get_current_level()`: 获取当前关卡配置
- `enemy_killed()`: 处理敌机被击败事件
- `update()`: 更新关卡状态

### 3. Player（玩家类）

**职责**: 玩家飞机的控制和状态管理

**核心属性**:
- `lives`: 生命值（初始3）
- `speed`: 移动速度
- `last_shot`: 上次射击时间（用于冷却）

**核心方法**:
- `update()`: 处理键盘输入，更新位置
- `shoot()`: 发射子弹（带冷却机制）

### 4. Enemy（敌机类）

**职责**: 敌机的行为和属性管理

**核心属性**:
- `enemy_type`: 敌机类型（1-8）
- `hp`: 当前生命值
- `speed`: 移动速度
- `shoot_probability`: 每帧射击概率

**核心方法**:
- `update()`: 向下移动
- `shoot()`: 概率性射击
- `hit()`: 受到伤害，返回是否被摧毁

### 5. Bullet & EnemyBullet（子弹类）

**职责**: 子弹的移动和生命周期管理

**行为**:
- 匀速直线移动
- 离开屏幕自动销毁

### 6. Explosion（爆炸效果类）

**职责**: 爆炸动画的播放

**行为**:
- 帧动画播放（9帧）
- 播放完毕自动销毁

---

## 数据流转

### 1. 游戏初始化流程

```mermaid
sequenceDiagram
    participant Main as main.py
    participant Game as Game类
    participant Pygame as Pygame引擎
    participant LevelMgr as LevelManager
    participant Config as level_config

    Main->>Game: __init__()
    Game->>Pygame: pygame.init()
    Game->>Pygame: 创建窗口(800x600)
    Game->>Game: load_sounds()
    Game->>Game: 创建Player实例
    Game->>LevelMgr: 创建LevelManager
    LevelMgr->>Config: 加载关卡配置
    Game->>Pygame: 播放背景音乐
    Main->>Game: run()
```

### 2. 游戏主循环流程

```mermaid
graph LR
    Start([开始帧]) --> EventLoop[事件处理]
    EventLoop --> |空格键|PlayerShoot[玩家射击]
    EventLoop --> |R键|Restart[重新开始]
    EventLoop --> |ESC键|Quit[退出游戏]
    EventLoop --> Update[更新游戏状态]
    
    Update --> UpdateSprites[更新所有Sprite]
    UpdateSprites --> SpawnEnemy[生成敌机]
    SpawnEnemy --> EnemyShoot[敌机射击]
    EnemyShoot --> Collision[碰撞检测]
    
    Collision --> BulletHit{子弹击中敌机?}
    BulletHit --> |是|DestroyEnemy[摧毁敌机]
    DestroyEnemy --> AddScore[增加分数]
    AddScore --> CheckLevel[检查关卡进度]
    
    BulletHit --> |否|EnemyCollision{敌机碰撞玩家?}
    EnemyCollision --> |是|LoseLife[失去生命]
    LoseLife --> CheckGameOver{生命为0?}
    CheckGameOver --> |是|GameOver[游戏结束]
    CheckGameOver --> |否|Draw[渲染画面]
    
    EnemyCollision --> |否|Draw
    CheckLevel --> Draw
    
    Draw --> Display[显示到屏幕]
    Display --> End([结束帧])
```

### 3. 敌机生成流程

```mermaid
sequenceDiagram
    participant Game as Game循环
    participant LevelMgr as LevelManager
    participant Config as level_config
    participant Enemy as Enemy实例
    participant SpriteGroup as Sprite组

    Game->>Game: enemy_spawn_timer++
    Game->>LevelMgr: get_current_level()
    LevelMgr-->>Game: 返回关卡配置
    
    Game->>Game: 检查spawn_interval
    
    alt 到达生成时间
        Game->>Config: 获取enemy_types
        Config-->>Game: [1, 2, 3]
        Game->>Game: random.choice()
        Game->>Enemy: 创建Enemy(type)
        Enemy->>Config: 加载敌机配置
        Config-->>Enemy: HP/速度/射击概率等
        Enemy->>Enemy: 加载图片
        Game->>SpriteGroup: 添加到all_sprites
        Game->>SpriteGroup: 添加到enemies
    end
```

### 4. 碰撞检测流程

```mermaid
graph TB
    Start[碰撞检测开始] --> Check1[检测: 子弹 vs 敌机]
    
    Check1 --> Hit1{碰撞?}
    Hit1 --> |是|Damage[敌机HP-1]
    Damage --> Dead{HP <= 0?}
    Dead --> |是|Destroy1[摧毁敌机]
    Destroy1 --> Score[分数 += score]
    Score --> Explosion1[创建爆炸效果]
    Explosion1 --> Sound1[播放爆炸音]
    Sound1 --> LevelCheck[level_manager.enemy_killed]
    
    Dead --> |否|Check2[检测: 敌机子弹 vs 玩家]
    Hit1 --> |否|Check2
    
    Check2 --> Hit2{碰撞?}
    Hit2 --> |是|Life1[玩家lives-1]
    Life1 --> Explosion2[创建爆炸效果]
    Explosion2 --> Sound2[播放爆炸音]
    Sound2 --> GameOver1{lives <= 0?}
    GameOver1 --> |是|EndGame[game_over = True]
    
    GameOver1 --> |否|Check3[检测: 敌机 vs 玩家]
    Hit2 --> |否|Check3
    
    Check3 --> Hit3{碰撞?}
    Hit3 --> |是|Life2[玩家lives-1]
    Life2 --> Explosion3[创建爆炸效果]
    Explosion3 --> Sound3[播放爆炸音]
    Sound3 --> GameOver2{lives <= 0?}
    GameOver2 --> |是|EndGame2[game_over = True]
    
    GameOver2 --> |否|End[碰撞检测结束]
    Hit3 --> |否|End
    LevelCheck --> End
    EndGame --> End
    EndGame2 --> End
```

---

## 时序图

### 完整游戏循环时序图

```mermaid
sequenceDiagram
    autonumber
    participant User as 用户
    participant Event as 事件系统
    participant Game as Game主类
    participant Player as Player
    participant LevelMgr as LevelManager
    participant Enemy as Enemy精灵组
    participant Bullet as Bullet精灵组
    participant Renderer as 渲染系统
    
    loop 每帧循环 (60 FPS)
        User->>Event: 按键输入
        Event->>Game: 事件分发
        
        alt 按下空格
            Game->>Player: shoot()
            Player-->>Game: 返回Bullet实例
            Game->>Bullet: 添加到bullets组
            Game->>Game: 播放射击音效
        end
        
        Game->>Game: update()
        Game->>Player: update()
        Player->>Player: 处理移动
        
        Game->>LevelMgr: get_current_level()
        LevelMgr-->>Game: 返回关卡配置
        
        alt 到达生成时间
            Game->>Enemy: 创建新敌机
            Game->>Enemy: 添加到enemies组
        end
        
        Game->>Enemy: 遍历所有敌机
        Enemy->>Enemy: update() 向下移动
        Enemy->>Enemy: shoot() 概率射击
        Enemy-->>Game: 返回子弹或None
        
        Game->>Bullet: update所有子弹
        Bullet->>Bullet: 移动位置
        
        Game->>Game: 碰撞检测
        
        alt 子弹击中敌机
            Game->>Enemy: hit()
            Enemy-->>Game: 返回是否摧毁
            Game->>Game: score += enemy.score
            Game->>LevelMgr: enemy_killed()
            LevelMgr->>LevelMgr: kills_in_level++
            
            alt 达到通关条件
                LevelMgr->>LevelMgr: in_transition = True
            end
        end
        
        alt 敌机或子弹击中玩家
            Game->>Player: lives--
            alt lives <= 0
                Game->>Game: game_over = True
                Game->>Game: 停止背景音乐
                Game->>Game: 播放game_over音效
            end
        end
        
        Game->>LevelMgr: update()
        
        alt 在过渡状态
            LevelMgr->>LevelMgr: transition_timer--
            alt 过渡结束
                LevelMgr->>LevelMgr: current_level++
                LevelMgr->>LevelMgr: kills_in_level = 0
            end
        end
        
        Game->>Renderer: draw()
        Renderer->>Renderer: 绘制背景
        Renderer->>Renderer: 绘制所有sprite
        Renderer->>Renderer: 绘制UI
        
        alt 在过渡状态
            Renderer->>Renderer: 绘制过渡动画
        end
        
        alt game_over
            Renderer->>Renderer: 绘制游戏结束画面
        else 通关所有关卡
            Renderer->>Renderer: 绘制通关画面
        end
        
        Renderer->>User: 显示画面
    end
```

---

## 设计模式

### 1. 组合模式（Sprite Group）

使用Pygame的Sprite组管理所有游戏对象：

```python
# 统一管理
self.all_sprites = pygame.sprite.Group()
self.enemies = pygame.sprite.Group()
self.bullets = pygame.sprite.Group()

# 统一更新
self.all_sprites.update()

# 统一渲染
self.all_sprites.draw(self.screen)
```

### 2. 工厂模式（敌机创建）

根据配置动态创建不同类型的敌机：

```python
def spawn_enemy(self):
    level = self.level_manager.get_current_level()
    enemy_type = random.choice(level['enemy_types'])
    enemy = Enemy(enemy_type)  # 工厂方法
```

### 3. 状态模式（关卡管理）

关卡管理器维护游戏状态：

```python
class LevelManager:
    - 正常状态: in_transition = False
    - 过渡状态: in_transition = True
    - 通关状态: current_level >= len(LEVELS)
```

### 4. 观察者模式（事件处理）

Pygame事件系统作为发布者，Game类作为订阅者：

```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        # 处理事件
```

### 5. 单例模式（Game类）

整个游戏只有一个Game实例控制全局：

```python
if __name__ == '__main__':
    game = Game()  # 唯一实例
    game.run()
```

---

## 配置系统

### 配置分离原则

关卡和敌机配置独立于游戏逻辑：

```python
# level_config.py
ENEMY_TYPES = {1: {...}, 2: {...}, ...}
LEVELS = [{...}, {...}, ...]

# main.py
from level_config import ENEMY_TYPES, LEVELS
```

**优势**:
- 修改游戏难度无需改动代码
- 易于扩展新关卡和敌机
- 数据驱动设计

---

## 性能优化策略

### 1. 对象池（隐式）

Sprite的kill()方法和Group管理实现了对象的自动回收。

### 2. 碰撞检测优化

使用Pygame的内置碰撞检测函数（基于矩形碰撞）：

```python
pygame.sprite.groupcollide()  # 组与组碰撞
pygame.sprite.spritecollide()  # 精灵与组碰撞
```

### 3. 帧率控制

固定60 FPS确保游戏流畅且不占用过多CPU：

```python
self.clock.tick(FPS)  # 限制帧率
```

---

## 扩展性设计

### 易于扩展的部分

1. **新增敌机类型**: 只需在`level_config.py`中添加配置
2. **新增关卡**: 在`LEVELS`列表中添加新配置
3. **新增道具**: 创建新的Sprite类，添加到碰撞检测
4. **新增BOSS战**: 修改关卡配置，添加特殊逻辑

### 扩展示例

添加道具系统：

```python
# 1. 创建道具类
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        # 实现道具逻辑
        
# 2. 添加到Game类
self.powerups = pygame.sprite.Group()

# 3. 碰撞检测
hits = pygame.sprite.spritecollide(
    self.player, self.powerups, True
)
```

---

## 总结

本游戏采用**分层架构**和**面向对象设计**，将复杂的游戏逻辑拆分为独立的模块和类。通过**配置分离**实现数据驱动，使用**Sprite组**统一管理游戏对象，通过**事件循环**驱动整个游戏流程。

**核心优势**:
- ✅ 结构清晰，易于理解
- ✅ 模块解耦，易于维护
- ✅ 配置驱动，易于扩展
- ✅ 性能良好，流畅运行

---

**文档版本**: 1.0  
**创建时间**: 2026年2月9日  
**作者**: CodeFlicker AI Assistant
