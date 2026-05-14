# Лабораторная работа №4
## Паттерн «Фиктивная служба» (Service Stub): Сервис покупки экзаменационных оценок

# Предметная область

Паттерн **«Фиктивная служба» (Service Stub)** используется для имитации работы внешнего сервиса без подключения к реальной системе. 

В качестве предметной области выбран **сервис покупки экзаменационных оценок**.

Пользователь может:

*ввести данные студента
*выбрать предмет
*выбрать преподавателя
*выбрать желаемую оценку
*оплатить услугу банковской картой
*получить чек об оплате

При этом реальная банковская система отсутствует.

Вместо неё используется **фиктивная служба оплаты**.

---
# Описание проблемы

Если реализовывать систему **без использования паттерна Service Stub**, возникают следующие проблемы:

## 1. Жёсткая связанность компонентов

Контроллер напрямую зависит от конкретной реализации оплаты:

```java
PaymentService paymentService
```
Вся логика:

проверки данных
обработки платежа
имитации банка

находится внутри одного класса.
## 2. Сложность подключения реального банка

При подключении настоящего банковского API пришлось бы:

изменять контроллер
менять бизнес-логику
переписывать существующий код

---


# Решение проблемы

## Использование паттерна Service Stub (Фиктивная служба)

Идея паттерна:

Создать интерфейс сервиса оплаты и отдельную фиктивную реализацию, имитирующую работу настоящего банка.

## Общий алгоритм раунда

MainController -> PaymentService -> StubPaymentService

Контроллер работает только с интерфейсом и не знает, какая реализация используется.

# Реализация без Service Stub

Вся логика находится в одном классе:

```java
@Service
public class PaymentService {

    public boolean processPayment(double amount) {

        return new Random().nextBoolean();
    }
}
```
Контроллер напрямую зависит от конкретного класса оплаты.

# Реализация с Service Stub



## Интерфейс — PaymentService

```java
public interface PaymentService {

    boolean processPayment(

            String surname,
            String name,
            String patronymic,
            String group,

            String subject,
            String teacher,

            int grade,

            String cardNumber,
            String cardHolder,
            String cvv
    );

    String getErrorMessage();
}
```

##  Конкретная реализация — StubPaymentService

```java
@Service
public class StubPaymentService
        implements PaymentService {

    private String errorMessage = "";

    @Override
    public boolean processPayment(

            String surname,
            String name,
            String patronymic,
            String group,

            String subject,
            String teacher,

            int grade,

            String cardNumber,
            String cardHolder,
            String cvv
    ) {

        System.out.println(
                "Фиктивная служба банка обрабатывает платёж..."
        );

        try {

            Thread.sleep(2000);

        } catch (Exception e) {

            e.printStackTrace();
        }

        if (cardNumber == null ||
                cardNumber.isBlank()) {

            errorMessage =
                    "Не указан номер карты";

            return false;
        }

        String cleanedCard =
                cardNumber.replace(" ", "");

        if (cleanedCard.length() != 16) {

            errorMessage =
                    "Номер карты должен содержать 16 цифр";

            return false;
        }

        errorMessage = "";

        return true;
    }

    @Override
    public String getErrorMessage() {

        return errorMessage;
    }
}
```
