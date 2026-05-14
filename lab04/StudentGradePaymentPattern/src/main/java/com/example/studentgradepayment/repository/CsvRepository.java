package com.example.studentgradepayment.repository;

import com.example.studentgradepayment.model.Order;
import com.example.studentgradepayment.model.SubjectTeacher;

import org.springframework.stereotype.Repository;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

@Repository
public class CsvRepository {

    private final String DB_FILE =
            "src/main/resources/DB.csv";

    private final String ORDERS_FILE =
            "src/main/resources/orders.csv";

    public List<SubjectTeacher> loadData() {

        List<SubjectTeacher> list =
                new ArrayList<>();

        try (BufferedReader reader =
                     new BufferedReader(
                             new FileReader(DB_FILE))) {

            String line;

            reader.readLine();

            while ((line = reader.readLine()) != null) {

                String[] parts =
                        line.split(",");

                list.add(
                        new SubjectTeacher(
                                parts[0],
                                parts[1]
                        )
                );
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        return list;
    }

    public void saveOrder(Order order) {

        try (FileWriter writer =
                     new FileWriter(
                             ORDERS_FILE,
                             true
                     )) {

            writer.append(order.toCsv());
            writer.append("\n");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}