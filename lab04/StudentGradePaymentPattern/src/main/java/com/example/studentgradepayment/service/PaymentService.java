package com.example.studentgradepayment.service;

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