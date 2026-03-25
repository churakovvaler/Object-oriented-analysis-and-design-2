#pragma once

#include "CompanyComponent.h"
#include <vector>
#include <string>

class Department : public CompanyComponent{

public:

    std::string name;

    std::vector<CompanyComponent*> children;

    Department(std::string n){
        name = n;
    }

    std::string getName() override{
        return name;
    }

    void add(CompanyComponent* component) override{
        children.push_back(component);
    }

    std::vector<CompanyComponent*> getChildren() override{
        return children;
    }

};