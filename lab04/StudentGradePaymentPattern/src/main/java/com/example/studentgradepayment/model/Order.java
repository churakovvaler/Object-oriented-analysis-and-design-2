package com.example.studentgradepayment.model;

public class Order {

    private String surname;
    private String name;
    private String patronymic;
    private String group;

    private String subject;
    private String teacher;

    private int grade;

    private double price;

    private String status;

    public Order(
            String surname,
            String name,
            String patronymic,
            String group,
            String subject,
            String teacher,
            int grade,
            double price,
            String status
    ) {

        this.surname = surname;
        this.name = name;
        this.patronymic = patronymic;
        this.group = group;

        this.subject = subject;
        this.teacher = teacher;

        this.grade = grade;

        this.price = price;

        this.status = status;
    }

    public String toCsv() {

        return surname + "," +
                name + "," +
                patronymic + "," +
                group + "," +
                subject + "," +
                teacher + "," +
                grade + "," +
                price + "," +
                status;
    }

    public String getSurname() {
        return surname;
    }

    public String getName() {
        return name;
    }

    public String getPatronymic() {
        return patronymic;
    }

    public String getGroup() {
        return group;
    }

    public String getSubject() {
        return subject;
    }

    public String getTeacher() {
        return teacher;
    }

    public int getGrade() {
        return grade;
    }

    public double getPrice() {
        return price;
    }

    public String getStatus() {
        return status;
    }
}