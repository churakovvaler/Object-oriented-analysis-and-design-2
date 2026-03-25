document.addEventListener("DOMContentLoaded", () => {

    const tree = document.getElementById("tree");
    const free = document.getElementById("freeEmployees");
    const select = document.getElementById("departmentSelect");

    const form = document.getElementById("employeeForm");
    const depBtn = document.getElementById("addDepBtn");


    /* ---------- DATE LIMIT ---------- */

    const birthInput = document.getElementById("empBirth");

    if(birthInput){

        const today = new Date();

        const maxDate = new Date(today.getFullYear()-18, today.getMonth(), today.getDate());
        const minDate = new Date(today.getFullYear()-100, today.getMonth(), today.getDate());

        birthInput.max = maxDate.toISOString().split("T")[0];
        birthInput.min = minDate.toISOString().split("T")[0];

    }


    /* ---------- ADD EMPLOYEE ---------- */

    if(form){

        form.addEventListener("submit", async function(e){

            e.preventDefault();

            const name = document.getElementById("empName").value;
            const pos = document.getElementById("empPosition").value;
            const birth = document.getElementById("empBirth").value;
            const exp = document.getElementById("empExp").value;
            const dep = document.getElementById("departmentSelect").value;
            const info = document.getElementById("empInfo").value;

            await fetch(`/add_employee?name=${encodeURIComponent(name)}&position=${encodeURIComponent(pos)}&birth=${birth}&experience=${exp}&info=${encodeURIComponent(info)}&department=${encodeURIComponent(dep)}`);

            form.reset();

            loadData();

        });

    }


    /* ---------- ADD DEPARTMENT ---------- */

    if(depBtn){

        depBtn.onclick = async () => {

            const name=document.getElementById("depName").value;

            if(!name) return;

            await fetch(`/add_department?name=${encodeURIComponent(name)}`);

            document.getElementById("depName").value="";

            loadData();

        };

    }


    /* ---------- FREE ZONE DROP ---------- */

    free.addEventListener("dragover", e=>{

        e.preventDefault();
        e.dataTransfer.dropEffect="move";

    });

    free.addEventListener("drop", async e=>{

        e.preventDefault();

        const id = e.dataTransfer.getData("id");

        await fetch(`/move_employee_free?id=${id}`);

        loadData();

    });


    /* ---------- LOAD DATA ---------- */

    async function loadData(){

        const res = await fetch("/data");
        const data = await res.json();

        tree.innerHTML="";
        free.innerHTML="";
        select.innerHTML='<option value="">No department</option>';


        /* ---------- DEPARTMENTS ---------- */

        data.departments.forEach(dep=>{

            const depDiv=document.createElement("div");
            depDiv.className="department";

            depDiv.innerHTML=`
<h3>

📂 ${dep.name}

<span>

<a href="#" onclick="deleteDepartment('${dep.name}')">🗑</a>

<a href="#" onclick="deleteDepartmentFull('${dep.name}')">💀</a>

</span>

</h3>
`;

            depDiv.addEventListener("dragover", e=>{

                e.preventDefault();
                e.dataTransfer.dropEffect="move";

            });

            depDiv.addEventListener("drop", async e=>{

                e.preventDefault();

                const id=e.dataTransfer.getData("id");

                await fetch(`/move_employee?id=${id}&department=${encodeURIComponent(dep.name)}`);

                loadData();

            });


            const ul=document.createElement("ul");

            dep.employees.forEach(emp=>{

                const li=document.createElement("li");

                li.draggable=true;

                li.addEventListener("dragstart", e=>{

                    e.dataTransfer.setData("id", emp.id);
                    e.dataTransfer.effectAllowed="move";

                });

                li.innerHTML=`

<div class="employee-card">

<div>
<b>Работник:</b> ${emp.name}<br>
<b>Позиция:</b> ${emp.position}<br>
<b>Опыт:</b> ${emp.experience ?? "-"}<br>
<b>ДР:</b> ${emp.birth ?? "-"}
</div>

<div class="emp-buttons">

<button onclick="showInfo(${JSON.stringify(emp.info ?? "")})">📓</button>

<a href="#" onclick="deleteEmployee(${emp.id})">❌</a>

</div>

</div>
`;

                ul.appendChild(li);

            });

            depDiv.appendChild(ul);
            tree.appendChild(depDiv);


            const opt=document.createElement("option");
            opt.value=dep.name;
            opt.text=dep.name;

            select.appendChild(opt);

        });


        /* ---------- FREE EMPLOYEES ---------- */

        data.freeEmployees.forEach(emp=>{

            const div=document.createElement("div");

            div.className="department";
            div.draggable=true;

            div.addEventListener("dragstart", e=>{

                e.dataTransfer.setData("id", emp.id);
                e.dataTransfer.effectAllowed="move";

            });

            div.innerHTML=`

<div class="employee-card">

<div>
<b>Работник:</b> ${emp.name}<br>
<b>Позиция:</b> ${emp.position}<br>
<b>Опыт:</b> ${emp.experience ?? "-"}<br>
<b>ДР:</b> ${emp.birth ?? "-"}
</div>

<div class="emp-buttons">

<button onclick="showInfo(${JSON.stringify(emp.info ?? "")})">📓</button>

<a href="#" onclick="deleteEmployee(${emp.id})">❌</a>

</div>

</div>
`;

            free.appendChild(div);

        });

    }


    /* ---------- INFO ---------- */

    window.showInfo = function(info){

        if(!info) info="No additional information";

        alert(info);

    };


    /* ---------- DELETE ---------- */

    window.deleteEmployee = async function(id){

        await fetch(`/delete_employee?id=${id}`);

        loadData();

    };

    window.deleteDepartment = async function(name){

        await fetch(`/delete_department?name=${encodeURIComponent(name)}`);

        loadData();

    };

    window.deleteDepartmentFull = async function(name){

        await fetch(`/delete_department_full?name=${encodeURIComponent(name)}`);

        loadData();

    };


    loadData();

});