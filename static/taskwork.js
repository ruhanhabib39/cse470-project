const getWorkers = (taskURL0, taskIDs_, csrfToken) => {
    const taskURL = taskURL0.substring(0, taskURL0.length - 2);
    const taskIDs = taskIDs_;

    const parser = new DOMParser();

    const getTaskDiv = (taskID) => document.getElementById(`task${taskID}`);

    const getTaskLink = (taskID) => `${taskURL}/${taskID}`;

    const attachListeners = (taskID, taskDiv) => {
        // listener for update button
        let updateButton = taskDiv.querySelector('.update-button');
        updateButton.addEventListener("click", () => updateTask(taskID));

        // listener for complete button
        let completeButton = taskDiv.querySelector('.complete-button');
        if (completeButton !== null && completeButton !== undefined) {
            completeButton.addEventListener("click", () => completeTask(taskID));
        }

        // listener for file input
        let fileInput = taskDiv.querySelector('.file-input');
        let fileName = taskDiv.querySelector('.file-name')
        fileInput.addEventListener("change", () => {
            const newName = fileInput.files[0] === undefined ? "" : fileInput.files[0].name;
            fileName.innerHTML = newName;
        });
    };

    // given task id, returns a Promise for the response div
    const queryTask = async (taskID, priority) => {

        if (priority === undefined || priority === null) {
            priority = "auto";
        }

        let response = await fetch(getTaskLink(taskID), {priority:priority});
        const text = await response.text();

        const responseHTML = parser.parseFromString(text, "text/html");
        const responseDiv = responseHTML.querySelector(`#task${taskID}`);

        attachListeners(taskID, responseDiv);

        return responseDiv;
    };


    const refreshTask = (taskID, priority) => {
        queryTask(taskID, priority)
            .then(responseDiv => {
                let taskDiv = getTaskDiv(taskID);
                taskDiv.parentNode.replaceChild(responseDiv, taskDiv);
            });

    };

    const refreshTasks = (preferredTaskID) => {
        if (preferredTaskID !== undefined && preferredTaskID !== null) {
            refreshTask(preferredTaskID, 'high');
        }
        for (const taskID of taskIDs) {
            if (taskID === preferredTaskID) {
                continue;
            }
            refreshTask(taskID, 'low');
        }
    };

    const initTasks = () => {
        document.addEventListener("DOMContentLoaded", () => {
            let taskColumn = document.getElementById("task_column");
            let taskPromises = taskIDs.map((id, index) => queryTask(id));
            Promise.all(taskPromises)
                .then(taskDivs => {
                    taskDivs.forEach(taskDiv => {
                        taskColumn.appendChild(taskDiv)
                    })
                });
        });
    };

    const updateTask = (taskID) => {
        // console.log(`update task called for ${taskID}`);
        const taskDiv = getTaskDiv(taskID);
        const taskLink = getTaskLink(taskID);
        const form = document.getElementById(`form${taskID}`);
        const data = new FormData(form);

        // console.log(Array.from(data));

        fetch(taskLink, { method: 'POST', body: data })
            .then(response => {
                refreshTasks(taskID);
            });
    };

    const completeTask = (taskID) => {
        const taskDiv = getTaskDiv(taskID);
        const taskLink = getTaskLink(taskID) + "/completed";
        const form = taskDiv.querySelector('.update-form');
        const data = new Formdata(form);

        fetch(taskLink, { method: 'POST', body: data })
            .then(response => refreshTasks(taskID));
    };

    const exported = {
        initTasks: initTasks, 
    };

    return exported;
};

