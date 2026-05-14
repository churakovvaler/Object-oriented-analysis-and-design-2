package com.example.studentgradepayment.service;

import org.springframework.stereotype.Service;

@Service
public class PaymentService {

    private String errorMessage = "";

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

        if (surname == null || surname.isBlank()) {

            errorMessage =
                    "Не указана фамилия";

            return false;
        }

        if (name == null || name.isBlank()) {

            errorMessage =
                    "Не указано имя";

            return false;
        }

        if (patronymic == null || patronymic.isBlank()) {

            errorMessage =
                    "Не указано отчество";

            return false;
        }

        if (group == null || group.isBlank()) {

            errorMessage =
                    "Не указана группа";

            return false;
        }

        if (subject == null || subject.isBlank()) {

            errorMessage =
                    "Не выбран предмет";

            return false;
        }

        if (teacher == null || teacher.isBlank()) {

            errorMessage =
                    "Не выбран преподаватель";

            return false;
        }

        if (grade < 3 || grade > 5) {

            errorMessage =
                    "Не выбрана оценка";

            return false;
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

        if (surname.length() < 2) {

            errorMessage =
                    "Фамилия слишком короткая";

            return false;
        }

        if (cvv.length() != 3) {

            errorMessage =
                    "CVV должен содержать 3 цифры";

            return false;
        }

        errorMessage = "";

        return true;
    }

    public String getErrorMessage() {

        return errorMessage;
    }
}