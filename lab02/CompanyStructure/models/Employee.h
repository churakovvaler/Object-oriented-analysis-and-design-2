#pragma once
#include <string>

class Employee {
public:

    int id;
    std::string fullName;
    std::string position;
    std::string birthDate;
    int experience;
    double salary;

    Employee(
            int id,
            const std::string& fullName,
            const std::string& position,
            const std::string& birthDate,
            int experience,
            double salary
    )
            : id(id),
              fullName(fullName),
              position(position),
              birthDate(birthDate),
              experience(experience),
              salary(salary) {}
};