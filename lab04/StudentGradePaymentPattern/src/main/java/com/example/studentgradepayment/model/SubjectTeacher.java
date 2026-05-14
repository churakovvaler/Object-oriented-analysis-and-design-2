package com.example.studentgradepayment.model;

public class SubjectTeacher {

    private String subject;
    private String teacher;

    public SubjectTeacher(String subject,
                          String teacher) {

        this.subject = subject;
        this.teacher = teacher;
    }

    public String getSubject() {
        return subject;
    }

    public String getTeacher() {
        return teacher;
    }
}