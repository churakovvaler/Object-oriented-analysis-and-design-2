# Лабораторная работа №3
## Паттерн «Шаблонный метод» (Template Method): Игра Blackjack

# Предметная область

Паттерн **«Шаблонный метод» (Template Method)** используется для определения **скелета алгоритма**, при этом отдельные шаги алгоритма могут переопределяться в подклассах.

В качестве предметной области выбрана **карточная игра Blackjack**.

Игровой процесс включает следующие этапы:

* Раздача карт
* Ход игрока
* Ход дилера
* Определение результата

Таким образом формируется **фиксированный алгоритм игрового раунда**.

---

# Описание проблемы

Если реализовывать игру **без использования паттерна Template Method**, возникают следующие проблемы:

## 1. Перемешанная логика

Вся логика игры находится в одном классе (`Game`):

* раздача карт
* обработка кликов
* логика дилера
* подсчет результата

Это нарушает принцип разделения ответственности.


## 2. Сложность понимания алгоритма

Алгоритм раунда не выделен явно, а распределён по условиям:

```python
if state == "player":
    ...
elif state == "dealer":
    ...
elif state == "end":
    ...
```

## 3. Плохая расширяемость

Добавление новых режимов игры требует изменения класса `Game`.

---


# Решение проблемы

## Использование паттерна Template Method (Шаблонный метод)

Идея паттерна:

Создать базовый класс, который задаёт **общий алгоритм игрового раунда**, а конкретные шаги реализовать в подклассах.

## Общий алгоритм раунда

```python
play_round():
    deal_cards()
    player_turn()
    dealer_turn()
    resolve_round()
```

Этот алгоритм не изменяется.

# Реализация без Template Method

Вся логика находится в одном классе:

```python
class Game:

    def update(self):
        if self.state == "dealer":
            if max(calculate_score(self.dealer)) < 17:
                self.dealer.append(self.deck.pop())
            else:
                # определение победителя
```


# Реализация с Template Method

<img width="661" height="384" alt="Диаграмма без названия drawio (6)" src="https://github.com/user-attachments/assets/67aad575-7b67-4b14-932c-fbc2f5737765" />

## Базовый класс — RoundTemplate

```python
class RoundTemplate(ABC):

    def play_round(self):
        self.deal_cards()
        self.player_turn()
        self.dealer_turn()
        self.resolve_round()

    @abstractmethod
    def deal_cards(self):
        pass

    @abstractmethod
    def player_turn(self):
        pass

    @abstractmethod
    def dealer_turn(self):
        pass

    @abstractmethod
    def resolve_round(self):
        pass
```

##  Конкретная реализация — BlackjackRound

```python
class BlackjackRound(RoundTemplate):

    def __init__(self, game):
        self.game = game

    def deal_cards(self):
        self.game.player = [self.game.deck.pop(), self.game.deck.pop()]
        self.game.dealer = [self.game.deck.pop(), self.game.deck.pop()]

    def player_turn(self):
        self.game.state = "player"

    def dealer_turn(self):
        while max(calculate_score(self.game.dealer)) < 17:
            self.game.dealer.append(self.game.deck.pop())

    def resolve_round(self):
        player_best = max(
            [s for s in calculate_score(self.game.player) if s <= 21],
            default=0
        )
        dealer_best = max(
            [s for s in calculate_score(self.game.dealer) if s <= 21],
            default=0
        )

        if dealer_best > 21 or player_best > dealer_best:
            self.game.stack += self.game.bet
            self.game.message = "Ты выиграл!"
        elif player_best == dealer_best:
            self.game.message = "Ничья"
        else:
            self.game.stack -= self.game.bet
            self.game.message = "Ты проиграл"
```
