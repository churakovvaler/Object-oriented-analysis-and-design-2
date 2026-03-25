document.addEventListener("DOMContentLoaded", () => {

    const tree = document.getElementById("tree");
    const free = document.getElementById("freeEmployees");
    const select = document.getElementById("departmentSelect");

    const form = document.getElementById("employeeForm");
    const depBtn = document.getElementById("addDepBtn");

    /* ---------- ограничение даты ---------- */

    const birthInput = document.getElementById("empBirth");

    if(birthInput){

        const today = new Date();

        const maxDate = new Date(today.getFullYear()-18, today.getMonth(), today.getDate());
        const minDate = new Date(today.getFullYear()-100, today.getMonth(), today.getDate());

        birthInput.max = maxDate.toISOString().split("T")[0];
        birthInput.min = minDate.toISOString().split("T")[0];

    }


    /* ---------- form submit ---------- */

    if(form){

        form.addEventListener("submit", async function(e){

            e.preventDefault();

            const name = document.getElementById("empName").value;
            const pos = document.getElementById("empPosition").value;
            const birth = document.getElementById("empBirth").value;
            const exp = document.getElementById("empExp").value;
            const dep = document.getElementById("departmentSelect").value;
            const info = document.getElementById("empInfo").value;

            /* возраст */

            const birthDate = new Date(birth);
            const today = new Date();

            const age = today.getFullYear() - birthDate.getFullYear();

            if(age < 18 || age > 100){

                alert("Employee must be between 18 and 100 years old");
                return;

            }

            /* опыт */

            if(!/^[0-9]+$/.test(exp)){

                alert("Experience must be a number");
                return;

            }

            /* отправка */

            await fetch(`/add_employee?name=${encodeURIComponent(name)}&position=${encodeURIComponent(pos)}&birth=${birth}&experience=${exp}&info=${encodeURIComponent(info)}&department=${encodeURIComponent(dep)}`);

            form.reset();

            loadData();

        });

    }


    /* ---------- add department ---------- */

    if(depBtn){

        depBtn.onclick = async () => {

            const name=document.getElementById("depName").value;

            if(!name) return;

            await fetch(`/add_department?name=${encodeURIComponent(name)}`);

            document.getElementById("depName").value="";

            loadData();

        };

    }


    /* ---------- drop free employees ---------- */

    free.addEventListener("dragover", e=>{
        e.preventDefault();
    });

    free.addEventListener("drop", async e=>{

        e.preventDefault();

        const id = e.dataTransfer.getData("id");

        await fetch(`/move_employee_free?id=${id}`);

        loadData();

    });


    /* ---------- load data ---------- */

    async function loadData(){

        const res = await fetch("/data");
        const data = await res.json();

        tree.innerHTML="";
        free.innerHTML="";
        select.innerHTML='<option value="">No department</option>';


        /* departments */

        data.departments.forEach(dep=>{

            const depDiv=document.createElement("div");
            depDiv.className="department";

            depDiv.innerHTML=
                `<h3>📂 ${dep.name}
<a href="#" onclick="deleteDepartment('${dep.name}')">🗑</a>
<a href="#" onclick="deleteDepartmentFull('${dep.name}')">💀</a>
</h3>`;

            depDiv.addEventListener("dragover", e=>e.preventDefault());

            depDiv.addEventListener("drop", async e=>{

                e.preventDefault();

                const id=e.dataTransfer.getData("id");

                await fetch(`/move_employee?id=${id}&department=${dep.name}`);

                loadData();

            });

            const ul=document.createElement("ul");

            dep.employees.forEach(emp=>{

                const li=document.createElement("li");

                li.draggable=true;

                li.addEventListener("dragstart", e=>{
                    e.dataTransfer.setData("id", emp.id);
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

<button onclick="showInfo('${emp.info ?? ""}')">📓</button>

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


        /* free employees */

        data.freeEmployees.forEach(emp=>{

            const div=document.createElement("div");

            div.className="department";
            div.draggable=true;

            div.addEventListener("dragstart", e=>{
                e.dataTransfer.setData("id", emp.id);
            });

            div.innerHTML=`
<div class="employee-card">

<div>
<b>Работник:</b> ${emp.name}<br>
<b>Позиция:</b> ${emp.position}
</div>

<div class="emp-buttons">
<button onclick="showInfo('${emp.info ?? ""}')">📓</button>
<a href="#" onclick="deleteEmployee(${emp.id})">❌</a>
</div>

</div>
`;

            free.appendChild(div);

        });

    }


    /* ---------- extra info ---------- */

    window.showInfo = function(info){

        if(!info) info="No additional information";

        alert(info);

    };


    /* ---------- delete ---------- */

    window.deleteDepartment = async function(name){

        await fetch(`/delete_department?name=${encodeURIComponent(name)}`);

        loadData();

    };

    window.deleteDepartmentFull = async function(name){

        await fetch(`/delete_department_full?name=${encodeURIComponent(name)}`);

        loadData();

    };

    window.deleteEmployee = async function(id){

        await fetch(`/delete_employee?id=${id}`);

        loadData();

    };


    loadData();

});