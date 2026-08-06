let editor;

window.addEventListener("DOMContentLoaded", function () {

    const textarea = document.getElementById("sql-editor");

    const savedQuery = localStorage.getItem(

        "cloudbuild-last-query"

    );

    if (

        savedQuery !== null &&

        savedQuery.trim() !== ""

    ) {

        textarea.value = savedQuery;

    }

    editor = CodeMirror.fromTextArea(

        textarea,

        {

            mode: "text/x-pgsql",

            lineNumbers: true,

            indentUnit: 4,

            matchBrackets: true,

            autoCloseBrackets: true,

            lineWrapping: true,

            theme: "default"

        }

    );
    
    
    
    
    
    const savedTheme =

        localStorage.getItem(

            "editor-theme"

        ) || "default";

    editor.setOption(

        "theme",

        savedTheme

    );

    if (savedTheme === "dracula") {

        document.getElementById(

            "theme-toggle"

        ).innerHTML = "☀ Light";

    }
    
    
    
    
    
    
    
    
    editor.setOption("extraKeys", {

        "Ctrl-Enter": function () {

            document.getElementById(

                "query-form"

            ).requestSubmit();

        },

        "Alt-Enter": function () {

            toggleFullScreen();

        },

        "Esc": function () {

            const wrapper = document.getElementById(

                "editor-wrapper"

            );

            if (wrapper.classList.contains(

                "editor-fullscreen"

            )) {

                wrapper.classList.remove(

                    "editor-fullscreen"

                );

                editor.refresh();

            }

        }

    });





    
    updateEditorStatus();

        editor.on(

            "change",

            function () {

                updateEditorStatus();

                localStorage.setItem(

                    "cloudbuild-last-query",

                    editor.getValue()

                );

            }

        );

        editor.on(

            "cursorActivity",

            updateEditorStatus

        );
        
        
        

    const form = document.getElementById("query-form");

    form.addEventListener(

        "submit",

        function(event) {

            if (!validateQuery()) {

                event.preventDefault();

                return;

            }

            editor.save();

        }

    );

});







function clearEditor() {

    if (

        !confirm(

            "Clear the editor?"

        )

    ) {

        return;

    }

    editor.setValue("");

    localStorage.removeItem(

        "cloudbuild-last-query"

    );

    editor.focus();

}






function saveQuery() {

    const form = document.getElementById("save-query-form");

    if (!form) {

        alert("Execute a query before saving.");

        return;

    }

    form.scrollIntoView({

        behavior: "smooth",

        block: "start"

    });

    const input = form.querySelector("input[name='query_name']");

    if (input) {

        input.focus();

    }

}







function formatSQL() {

    if (!editor) {

        return;

    }

    try {

        const formatted = sqlFormatter.format(

            editor.getValue(),

            {

                language: "postgresql"

            }

        );

        editor.setValue(formatted);

    }

    catch (error) {

        alert("Unable to format SQL.");

    }

}





function exportCSV() {

    if (!editor) {

        alert("Editor not initialized.");

        return;

    }

    const query = editor.getValue().trim();

    if (query === "") {

        alert("Please enter a SQL query.");

        return;

    }

    document.getElementById("export-query").value = query;

    document.getElementById("export-form").submit();

}







function validateQuery() {

    const query = editor.getValue().trim();

    if (query === "") {

        alert("Please enter a SQL query.");

        return false;

    }

    const forbidden = [

        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "TRUNCATE",
        "ALTER",
        "CREATE",
        "GRANT",
        "REVOKE",
        "VACUUM"

    ];

    const upperQuery = query.toUpperCase();

    for (const keyword of forbidden) {

        if (upperQuery.includes(keyword)) {

            alert(

                keyword +

                " statements are not allowed."

            );

            return false;

        }

    }

    return true;

}






function updateEditorStatus() {

    if (!editor) {

        return;

    }

    const text = editor.getValue();

    document.getElementById("char-count").textContent =

        text.length;

    document.getElementById("line-count").textContent =

        editor.lineCount();

    const cursor = editor.getCursor();

    document.getElementById("cursor-position").textContent =

        (cursor.line + 1) +

        " : " +

        (cursor.ch + 1);

}




editor.focus();




function toggleTheme() {

    const current = editor.getOption("theme");

    if (current === "default") {

        editor.setOption("theme", "dracula");

        localStorage.setItem(

            "editor-theme",

            "dracula"

        );

        document.getElementById(

            "theme-toggle"

        ).innerHTML = "☀ Light";

    }

    else {

        editor.setOption(

            "theme",

            "default"

        );

        localStorage.setItem(

            "editor-theme",

            "default"

        );

        document.getElementById(

            "theme-toggle"

        ).innerHTML = "🌙 Dark";

    }

}





function toggleFullScreen() {

    const wrapper = document.getElementById(

        "editor-wrapper"

    );

    wrapper.classList.toggle(

        "editor-fullscreen"

    );

    setTimeout(function () {

        editor.refresh();

        editor.focus();

    }, 100);
}






function loadRecentQuery(query) {

    editor.setValue(query);

    editor.focus();

}






