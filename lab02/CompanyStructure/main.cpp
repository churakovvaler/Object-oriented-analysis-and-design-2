#include <iostream>
#include <vector>
#include <string>
#include "httplib.h"

using namespace httplib;
using namespace std;

struct Employee{

    int id;
    string name;
    string position;

    string birth;
    int experience;

    string info;

};

struct Department{
    string name;
    vector<Employee> employees;
};

vector<Department> departments;
vector<Employee> freeEmployees;

int employeeCounter = 1;


/* ---------- JSON ---------- */

string getJSON(){

    string json="{\"departments\":[";

    for(int i=0;i<departments.size();i++){

        auto &d=departments[i];

        json+="{\"name\":\""+d.name+"\",\"employees\":[";

        for(int j=0;j<d.employees.size();j++){

            auto &e=d.employees[j];

            json+="{";
            json+="\"id\":"+to_string(e.id)+",";
            json+="\"name\":\""+e.name+"\",";
            json+="\"position\":\""+e.position+"\",";
            json+="\"birth\":\""+e.birth+"\",";
            json+="\"experience\":"+to_string(e.experience)+",";
            json+="\"info\":\""+e.info+"\"";
            json+="}";

            if(j<d.employees.size()-1) json+=",";
        }

        json+="]}";

        if(i<departments.size()-1) json+=",";
    }

    json+="],\"freeEmployees\":[";

    for(int i=0;i<freeEmployees.size();i++){

        auto &e=freeEmployees[i];

        json+="{";
        json+="\"id\":"+to_string(e.id)+",";
        json+="\"name\":\""+e.name+"\",";
        json+="\"position\":\""+e.position+"\",";
        json+="\"birth\":\""+e.birth+"\",";
        json+="\"experience\":"+to_string(e.experience)+",";
        json+="\"info\":\""+e.info+"\"";
        json+="}";

        if(i<freeEmployees.size()-1) json+=",";
    }

    json+="]}";

    return json;
}


/* ---------- SERVER ---------- */

int main(){

    Server svr;

    svr.set_mount_point("/", "../web");


    /* получить данные */

    svr.Get("/data",[](const Request&,Response&res){

        res.set_content(getJSON(),"application/json");

    });


    /* добавить департамент */

    svr.Get("/add_department",[](const Request&req,Response&res){

        Department d;
        d.name=req.get_param_value("name");

        departments.push_back(d);

        res.set_content("ok","text/plain");

    });


    /* удалить департамент */

    svr.Get("/delete_department",[](const Request&req,Response&res){

        string name=req.get_param_value("name");

        for(int i=0;i<departments.size();i++){

            if(departments[i].name==name){

                for(auto &e:departments[i].employees){
                    freeEmployees.push_back(e);
                }

                departments.erase(departments.begin()+i);

                break;
            }
        }

        res.set_content("ok","text/plain");

    });


    /* ---------- добавить сотрудника ---------- */

    svr.Get("/add_employee",[](const Request&req,Response&res){

        Employee e;

        e.id=employeeCounter++;

        e.name=req.get_param_value("name");
        e.position=req.get_param_value("position");

        e.birth=req.get_param_value("birth");

        if(req.has_param("experience"))
            e.experience=stoi(req.get_param_value("experience"));
        else
            e.experience=0;

        if(req.has_param("info"))
            e.info=req.get_param_value("info");
        else
            e.info="";

        string dep=req.get_param_value("department");


        if(dep==""){

            freeEmployees.push_back(e);

        }else{

            for(auto &d:departments){

                if(d.name==dep){

                    d.employees.push_back(e);
                    break;
                }
            }

        }

        res.set_content("ok","text/plain");

    });


    /* ---------- удалить сотрудника ---------- */

    svr.Get("/delete_employee",[](const Request&req,Response&res){

        int id=stoi(req.get_param_value("id"));

        for(auto &d:departments){

            for(int i=0;i<d.employees.size();i++){

                if(d.employees[i].id==id){

                    d.employees.erase(d.employees.begin()+i);

                    res.set_content("ok","text/plain");
                    return;
                }
            }
        }

        for(int i=0;i<freeEmployees.size();i++){

            if(freeEmployees[i].id==id){

                freeEmployees.erase(freeEmployees.begin()+i);
                break;
            }
        }

        res.set_content("ok","text/plain");

    });


    /* ---------- удалить департамент полностью ---------- */

    svr.Get("/delete_department_full", [](const Request& req, Response& res){

        string name = req.get_param_value("name");

        for(int i=0;i<departments.size();i++){

            if(departments[i].name == name){

                departments.erase(departments.begin() + i);
                break;
            }
        }

        res.set_content("ok","text/plain");

    });


    /* ---------- перемещение сотрудника ---------- */

    svr.Get("/move_employee",[](const Request&req,Response&res){

        int id=stoi(req.get_param_value("id"));
        string target=req.get_param_value("department");

        Employee moved;
        bool found=false;

        for(auto &d:departments){

            for(int i=0;i<d.employees.size();i++){

                if(d.employees[i].id==id){

                    moved=d.employees[i];

                    d.employees.erase(d.employees.begin()+i);

                    found=true;
                    break;
                }
            }

            if(found) break;
        }

        if(!found){

            for(int i=0;i<freeEmployees.size();i++){

                if(freeEmployees[i].id==id){

                    moved=freeEmployees[i];

                    freeEmployees.erase(freeEmployees.begin()+i);

                    found=true;
                    break;
                }
            }
        }

        for(auto &d:departments){

            if(d.name==target){

                d.employees.push_back(moved);
                break;
            }
        }

        res.set_content("ok","text/plain");

    });


    /* ---------- перемещение в свободные ---------- */

    svr.Get("/move_employee_free", [](const Request& req, Response& res){

        int id = stoi(req.get_param_value("id"));

        Employee moved;
        bool found = false;

        for(auto &d : departments){

            for(int i=0;i<d.employees.size();i++){

                if(d.employees[i].id == id){

                    moved = d.employees[i];
                    d.employees.erase(d.employees.begin()+i);

                    found = true;
                    break;
                }
            }

            if(found) break;
        }

        if(found){
            freeEmployees.push_back(moved);
        }

        res.set_content("ok","text/plain");

    });


    cout<<"Server started: http://localhost:8080/index.html\n";

    svr.listen("localhost",8080);
}