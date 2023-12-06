const getWorkers = (taskURL0, taskIDs_) => {
    const taskURL = taskURL0.substring(0, taskURL0.length - 2);
    const taskIDs = taskIDs_;

    console.log(taskURL);
    console.log(taskIDs);

    const getTaskDiv = (taskID) => document.getElementById(`task${taskID}`);

    const getTaskLink = (taskID) => `${taskURL}/${taskID}`;

    const refreshTask = (taskID) => {
        const taskDiv = getTaskDiv(taskID);
        fetch(getTaskLink(taskID))
                .then(response => response.text())
                .then(text => {
                    let responseDiv = document.createElement("div");
                    responseDiv.innerHTML = text;
                    taskDiv.innerHTML = responseDiv.children[0].innerHTML;
                });
    };

    const pushTask = (taskID) => {
        let taskColumn = document.getElementById(`task_column`);

        fetch(getTaskLink(taskID))
                .then(response => response.text())
                .then(text => taskColumn.innerHTML += text);
    };

    const initTasks = () => {
        document.addEventListener("DOMContentLoaded", () => {
            for (const taskID of taskIDs) {
                pushTask(taskID);
            }
        });
    };

    const updateTask = (taskID) => {
        const taskDiv = getTaskDiv(taskID);
        const form = document.getElementById(`form${taskID}`);
        const data = new FormData(form);
        const taskLink = getTaskLink(taskID);

        console.log(Array.from(data));

        fetch(taskLink, { method: 'POST', body: data })
            .then(response => { refreshTask(taskID); });
    };

    const exported = {
        refreshTask: refreshTask,
        pushTask: pushTask,
        initTasks: initTasks, 
        updateTask: updateTask,
    };

    return exported;
};

