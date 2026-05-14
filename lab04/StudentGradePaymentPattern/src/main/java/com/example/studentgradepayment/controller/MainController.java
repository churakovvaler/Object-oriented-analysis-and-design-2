package com.example.studentgradepayment.controller;

import com.example.studentgradepayment.model.Order;
import com.example.studentgradepayment.repository.CsvRepository;
import com.example.studentgradepayment.service.PaymentService;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class MainController {

    private final CsvRepository repository;
    private final PaymentService paymentService;

    public MainController(CsvRepository repository,
                          PaymentService paymentService) {

        this.repository = repository;
        this.paymentService = paymentService;
    }

    @GetMapping("/")
    public String index(Model model) {

        model.addAttribute(
                "items",
                repository.loadData()
        );

        return "index";
    }

    @PostMapping("/payment")
    public String paymentPage(

            @RequestParam String surname,
            @RequestParam String name,
            @RequestParam String patronymic,
            @RequestParam String group,

            @RequestParam String subject,
            @RequestParam String teacher,
            @RequestParam int grade,

            Model model) {

        double price = switch (grade) {

            case 3 -> 500;
            case 4 -> 750;
            default -> 1000;
        };

        model.addAttribute("surname", surname);
        model.addAttribute("name", name);
        model.addAttribute("patronymic", patronymic);
        model.addAttribute("group", group);

        model.addAttribute("subject", subject);
        model.addAttribute("teacher", teacher);

        model.addAttribute("grade", grade);
        model.addAttribute("price", price);

        return "payment";
    }

    @PostMapping("/pay")
    public String pay(

            @RequestParam String surname,
            @RequestParam String name,
            @RequestParam String patronymic,
            @RequestParam String group,

            @RequestParam String subject,
            @RequestParam String teacher,

            @RequestParam int grade,
            @RequestParam double price,

            @RequestParam String cardNumber,
            @RequestParam String cardHolder,
            @RequestParam String cvv,

            Model model) {

        boolean success =
                paymentService.processPayment(

                        surname,
                        name,
                        patronymic,
                        group,

                        subject,
                        teacher,

                        grade,

                        cardNumber,
                        cardHolder,
                        cvv
                );

        String status;

        if (success) {

            status = "ОПЛАЧЕНО";

        } else {

            status =
                    "ОШИБКА ОПЛАТЫ — " +
                            paymentService.getErrorMessage();
        }

        Order order = new Order(

                surname,
                name,
                patronymic,
                group,

                subject,
                teacher,

                grade,
                price,
                status
        );

        repository.saveOrder(order);

        model.addAttribute("order", order);

        return "receipt";
    }
}