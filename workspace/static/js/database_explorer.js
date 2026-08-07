/* ===========================================================
   CloudBuild - Database Explorer
=========================================================== */

let selectedObject = null;

document.addEventListener("DOMContentLoaded", function () {

    console.log("CloudBuild Explorer JS Loaded");

    const explorerItems = document.querySelectorAll(".explorer-object");
    
  
    
    const searchBox = document.getElementById("objectSearch");

    console.log("Explorer Objects :", explorerItems.length);

    /* ==========================================
       Object Click
    ========================================== */

    explorerItems.forEach(item => {

        item.addEventListener("click", function (e) {

            e.preventDefault();

            explorerItems.forEach(obj => {

                obj.classList.remove("active");

            });

            this.classList.add("active");
            
            selectedObject = {

                type: this.dataset.objectType,

                name: this.dataset.objectName

            };

            loadObject(

                this.dataset.objectType,

                this.dataset.objectName

            );

        });

    });

    
    /* ==========================================
   Live Search
    ========================================== */


    if (searchBox) {

        searchBox.addEventListener("input", function () {

            const keyword = this.value.trim().toLowerCase();

            explorerItems.forEach(item => {

                const objectName = item.dataset.objectName.toLowerCase();

                item.style.display = objectName.includes(keyword)
                ? ""
                    : "none";

            });

        });

    }
    
    const refreshButton = document.getElementById("refreshExplorer");

    if (refreshButton) {

        refreshButton.addEventListener("click", function () {

            location.reload();

        });

    }
    
    
    
const browseButton = document.getElementById("browseDataBtn");

if (browseButton) {

    browseButton.addEventListener("click", function () {

        if (!selectedObject) {

            alert("Select a table first.");

            return;

        }

        if (selectedObject.type !== "table") {

            alert("Browse Data is available only for tables.");

            return;

        }

        const sql =

`SELECT *

FROM ${selectedObject.name}

LIMIT 100;`;

        sessionStorage.setItem(

            "workspaceQuery",

            sql

        );

        window.location.href = "/sql-workspace";

    });

}    
    
    
    
    
    

});

/* ==========================================
   Placeholder
========================================== */

/* ==========================================
   Load Object Details
========================================== */

async function loadObject(type, name) {

    const panel = document.getElementById("detailsPanel");

    panel.innerHTML = `

        <div class="text-center p-5">

            <div class="spinner-border text-primary"></div>

            <p class="mt-3">

                Loading ${name}...

            </p>

        </div>

    `;

    try {

        const response = await fetch(

            `/object-details?type=${type}&name=${encodeURIComponent(name)}`

        );

        if (!response.ok) {

            throw new Error("Failed to load object details.");

        }

        const data = await response.json();

        let html = `

            <h3>${data.table}</h3>

            <table class="table table-bordered">

                <tr>

                    <th width="180">Schema</th>

                    <td>${data.schema}</td>

                </tr>

                <tr>

                    <th>Rows</th>

                    <td>${data.rows}</td>

                </tr>

            </table>

            <h4 class="mt-4">Columns</h4>

            <table class="table table-striped">

                <thead>

                    <tr>

                        <th>Name</th>

                        <th>Data Type</th>

                        <th>Nullable</th>

                    </tr>

                </thead>

                <tbody>

        `;

        data.columns.forEach(col => {

            html += `

                <tr>

                    <td>${col.name}</td>

                    <td>${col.type}</td>

                    <td>${col.nullable}</td>

                </tr>

            `;

        });

        html += `

                </tbody>

            </table>

        `;

        panel.innerHTML = html;

    }

    catch (error) {

        panel.innerHTML = `

            <div class="alert alert-danger">

                ${error.message}

            </div>

        `;

        console.error(error);

    }

}

document.addEventListener("DOMContentLoaded", function () {

    /* ============================
       View DDL
    ============================ */

    const ddlButton = document.getElementById("viewDDLBtn");

    if (ddlButton) {

        ddlButton.addEventListener("click", async function () {

            if (!selectedObject) {

                alert("Select a table first.");

                return;

            }

            try {

                const response = await fetch(
                    `/object-ddl?type=${selectedObject.type}&name=${encodeURIComponent(selectedObject.name)}`
                );

                if (!response.ok) {

                    throw new Error("Unable to load DDL.");

                }

                const data = await response.json();

                document.getElementById("ddlCode").textContent = data.ddl;

                document.getElementById("ddlPanel").style.display = "block";

                document.getElementById("ddlPanel").scrollIntoView({
                    behavior: "smooth"
                });

            }

            catch (err) {

                console.error(err);

                alert(err.message);

            }

        });

    }

    /* ============================
       Relationships
    ============================ */

    const relationButton = document.getElementById("relationshipsBtn");

if (relationButton) {

    relationButton.addEventListener("click", async function () {

        try {

            console.log("STEP 1");

            if (!selectedObject) {
                alert("Select a table first.");
                return;
            }

            console.log("STEP 2", selectedObject);

            const response = await fetch(
                `/object-relationships?name=${encodeURIComponent(selectedObject.name)}`
            );

            console.log("STEP 3", response.status);

            if (!response.ok) {
                throw new Error("Unable to load relationships.");
            }

            const data = await response.json();

            console.log("STEP 4", data);

            const body = document.getElementById("relationshipBody");

            body.innerHTML = "";

            if (data.length === 0) {

                body.innerHTML = `
                    <tr>
                        <td colspan="2" class="text-center text-muted">
                            No relationships found.
                        </td>
                    </tr>`;

            } else {

                data.forEach(rel => {

                    body.innerHTML += `
                        <tr>
                            <td>${rel.column}</td>
                            <td>${rel.table}.${rel.foreign_column}</td>
                        </tr>`;

                });

            }

            document.getElementById("relationshipPanel").style.display = "block";

            document.getElementById("relationshipPanel").scrollIntoView({
                behavior: "smooth"
            });

        }

        catch (err) {

            console.error(err);

        }

    });


}

});
