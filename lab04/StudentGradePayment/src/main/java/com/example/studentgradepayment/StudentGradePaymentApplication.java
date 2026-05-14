package com.example.studentgradepayment;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class StudentGradePaymentApplication {

    public static void main(String[] args) {

        SpringApplication.run(
                StudentGradePaymentApplication.class,
                args
        );

        System.out.println();
        System.out.println(
                "Приложение успешно запущено!"
        );

        System.out.println(
                "http://localhost:8080/"
        );

        System.out.println();
    }
}