#pragma once

#include <string>
#include <vector>

class CompanyComponent{

public:

    virtual std::string getName() = 0;

    virtual void add(CompanyComponent* component){}

    virtual std::vector<CompanyComponent*> getChildren(){
        return {};
    }

    virtual bool isEmployee(){
        return false;
    }

    virtual ~CompanyComponent(){}

};