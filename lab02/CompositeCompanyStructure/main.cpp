#include <iostream>
#include <vector>
#include <string>
#include "httplib.h"

#include "data/Company.h"
#include "models/Employee.h"

using namespace httplib;
using namespace std;

Company company;

vector<Employee*> freeEmployees;

int employeeCounter = 1;


/* ---------- FIND DEPARTMENT ---------- */

Department* findDepartment(Department* dep, string name){

    if(dep->name == name)
        return dep;

    for(auto child : dep->children){

        Department* d = dynamic_cast<Department*>(child);

        if(d){

            Department* result = findDepartment(d, name);

            if(result) return result;

        }
    }

    return nullptr;
}


/* ---------- FIND EMPLOYEE ---------- */

Employee* findAndRemoveEmployee(int id){

    /* ищем в свободных */

    for(int i=0;i<freeEmployees.size();i++){

        if(freeEmployees[i]->id == id){

            Employee* e = freeEmployees[i];

            freeEmployees.erase(freeEmployees.begin()+i);

            return e;
        }
    }

    /* ищем в департаментах */

    for(auto child : company.root.children){

        Department* d = dynamic_cast<Department*>(child);

        if(!d) continue;

        for(int i=0;i<d->children.size();i++){

            Employee* e = dynamic_cast<Employee*>(d->children[i]);

            if(e && e->id == id){

                d->children.erase(d->children.begin()+i);

                return e;
            }
        }
    }

    return nullptr;
}


/* ---------- JSON ---------- */

string employeeJSON(Employee* e){

    string json="{";

    json+="\"id\":"+to_string(e->id)+",";
    json+="\"name\":\""+e->name+"\",";
    json+="\"position\":\""+e->position+"\",";
    json+="\"birth\":\""+e->birth+"\",";
    json+="\"experience\":"+to_string(e->experience)+",";
    json+="\"info\":\""+e->info+"\"";

    json+="}";

    return json;
}


string departmentJSON(Department* dep){

    string json="{\"name\":\""+dep->name+"\",\"employees\":[";

    bool first=true;

    for(auto child:dep->children){

        Employee* e=dynamic_cast<Employee*>(child);

        if(e){

            if(!first) json+=",";
            json+=employeeJSON(e);

            first=false;

        }
    }

    json+="]}";

    return json;
}


string getJSON(){

    string json="{\"departments\":[";

    bool first=true;

    for(auto child:company.root.children){

        Department* d=dynamic_cast<Department*>(child);

        if(d){

            if(!first) json+=",";
            json+=departmentJSON(d);

            first=false;

        }
    }

    json+="],\"freeEmployees\":[";

    for(int i=0;i<freeEmployees.size();i++){

        json+=employeeJSON(freeEmployees[i]);

        if(i<freeEmployees.size()-1)
            json+=",";
    }

    json+="]}";

    return json;
}


/* ---------- SERVER ---------- */

int main(){

    Server svr;

    svr.set_mount_point("/", "../web");


    /* ---------- DATA ---------- */

    svr.Get("/data",[](const Request&,Response&res){

        res.set_content(getJSON(),"application/json");

    });


    /* ---------- ADD DEPARTMENT ---------- */

    svr.Get("/add_department",[](const Request&req,Response&res){

        string name=req.get_param_value("name");

        company.root.add(new Department(name));

        res.set_content("ok","text/plain");

    });


    /* ---------- ADD EMPLOYEE ---------- */

    svr.Get("/add_employee",[](const Request&req,Response&res){

        string name=req.get_param_value("name");
        string position=req.get_param_value("position");

        string birth=req.get_param_value("birth");

        int exp=stoi(req.get_param_value("experience"));

        string info=req.get_param_value("info");

        string dep=req.get_param_value("department");

        Employee* e=new Employee(

                employeeCounter++,
                name,
                position,
                birth,
                exp,
                info

        );

        if(dep==""){

            freeEmployees.push_back(e);

        }else{

            Department* d=findDepartment(&company.root,dep);

            if(d)
                d->add(e);

        }

        res.set_content("ok","text/plain");

    });


    /* ---------- MOVE EMPLOYEE ---------- */

    svr.Get("/move_employee",[](const Request&req,Response&res){

        int id = stoi(req.get_param_value("id"));
        string target = req.get_param_value("department");

        Employee* moved = findAndRemoveEmployee(id);

        if(moved){

            Department* dep = findDepartment(&company.root,target);

            if(dep)
                dep->add(moved);
        }

        res.set_content("ok","text/plain");

    });


    /* ---------- MOVE TO FREE ---------- */

    svr.Get("/move_employee_free",[](const Request&req,Response&res){

        int id = stoi(req.get_param_value("id"));

        Employee* moved = findAndRemoveEmployee(id);

        if(moved)
            freeEmployees.push_back(moved);

        res.set_content("ok","text/plain");

    });


    /* ---------- DELETE EMPLOYEE ---------- */

    svr.Get("/delete_employee",[](const Request&req,Response&res){

        int id = stoi(req.get_param_value("id"));

        Employee* e = findAndRemoveEmployee(id);

        if(e)
            delete e;

        res.set_content("ok","text/plain");

    });


    /* ---------- DELETE DEPARTMENT (transfer employees) ---------- */

    svr.Get("/delete_department",[](const Request&req,Response&res){

        string name=req.get_param_value("name");

        for(int i=0;i<company.root.children.size();i++){

            Department* d=dynamic_cast<Department*>(company.root.children[i]);

            if(d && d->name==name){

                for(auto child:d->children){

                    Employee* e=dynamic_cast<Employee*>(child);

                    if(e)
                        freeEmployees.push_back(e);
                }

                delete d;

                company.root.children.erase(company.root.children.begin()+i);

                break;
            }
        }

        res.set_content("ok","text/plain");

    });


    /* ---------- DELETE DEPARTMENT FULL ---------- */

    svr.Get("/delete_department_full",[](const Request&req,Response&res){

        string name=req.get_param_value("name");

        for(int i=0;i<company.root.children.size();i++){

            Department* d=dynamic_cast<Department*>(company.root.children[i]);

            if(d && d->name==name){

                delete d;

                company.root.children.erase(company.root.children.begin()+i);

                break;
            }
        }

        res.set_content("ok","text/plain");

    });


    cout<<"Server started: http://localhost:8080/index.html\n";

    svr.listen("localhost",8080);

}