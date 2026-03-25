#pragma once
#include <vector>
#include "Employee.h"

class Department {
public:

    std::string name;

    std::vector<Employee> employees;
    std::vector<Department> subDepartments;

    Department(const std::string& name) : name(name) {}

    void addEmployee(const Employee& emp) {
        employees.push_back(emp);
    }

    void addDepartment(const Department& dep) {
        subDepartments.push_back(dep);
    }

    void removeEmployee(int id){

        for(int i=0;i<employees.size();i++){

            if(employees[i].id == id){
                employees.erase(employees.begin()+i);
                break;
            }
        }
    }
};