#pragma once

#include "CompanyComponent.h"
#include <string>

class Employee : public CompanyComponent{

public:

    int id;

    std::string name;
    std::string position;

    std::string birth;
    int experience;

    std::string info;

    Employee(
            int i,
            std::string n,
            std::string p,
            std::string b,
            int exp,
            std::string inf
    ){

        id=i;
        name=n;
        position=p;

        birth=b;
        experience=exp;

        info=inf;
    }

    std::string getName() override{
        return name;
    }

    bool isEmployee() override{
        return true;
    }

};