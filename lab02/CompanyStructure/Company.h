#pragma once
#include "../models/Department.h"
#include <vector>

class Company {
public:

    Department root;

    std::vector<Employee> freeEmployees;

    Company() : root("Company") {}
};