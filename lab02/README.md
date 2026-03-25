# Лабораторная работа №2
## Паттерн «Компоновщик» (Composite): Структура компании

## Предметная область

Паттерн **«Компоновщик» (Composite)** используется для представления иерархических структур, где объекты могут содержать другие объекты того же типа.

В качестве предметной области выбрана **структура компании**.

В компании существует иерархия:

- Компания
- Департаменты
- Сотрудники

Таким образом формируется **древовидная структура организации**.


---

# Описание проблемы

Если реализовывать систему **без использования паттерна Composite**, возникнут следующие проблемы:

1. **Разные типы объектов**
   
   Департамент и сотрудник имеют разные структуры данных и методы.

2. **Сложность работы с иерархией**
   
   Код должен отдельно обрабатывать:
   - департаменты
   - сотрудников

3. **Усложнение логики**

   Например при обходе структуры компании нужно писать разные условия:

```cpp
if(object is Department)
{
    // обработка департамента
}
else if(object is Employee)
{
    // обработка сотрудника
}
```
4. **Плохая масштабируемость**

При добавлении новых типов элементов иерархии потребуется переписывать код.

# Решение проблемы

## Использование паттерна Composite (Компоновщик). 

Идея паттерна:

Создать общий базовый класс, который будет представлять любой элемент структуры.

В нашем случае это:
```cpp
CompanyComponent
```
От него наследуются:
```cpp
Department
Employee
```
Таким образом:

Department может содержать другие объекты типа CompanyComponent
Employee является листом дерева

Это позволяет работать с объектами единообразно.
# Реализация идеи без Composite   

## Employee

```cpp
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
```

## Department

```cpp
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
```

В системе использовались два основных контейнера:

vector<Department> departments; хранит все департаменты компании
vector<Employee> freeEmployees; хранит сотрудников без департамента

# Реализация идеи с Composite   

<img width="681" height="724" alt="2laba drawio" src="https://github.com/user-attachments/assets/2442efdb-66b6-4dd1-b229-b7568da3573b" />

## CompanyComponent

```cpp
class CompanyComponent
{
public:

    virtual string getName() = 0;

    virtual void add(CompanyComponent* component) {}

    virtual vector<CompanyComponent*> getChildren()
    {
        return {};
    }

};
```
## Department

```cpp
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
```

## Employee 

```cpp
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
```

## Company

```cpp

class Company{

public:

    Department root;

    Company() : root("Company") {}

};
```
