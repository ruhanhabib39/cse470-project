const getWorkers = (taskURL0, taskIDs_, taskRoots_) => {
    const taskURL = taskURL0.substring(0, taskURL0.length - 2);
    const taskIDs = taskIDs_;

    let taskForms = {};

    const getTaskDiv = (taskID) => document.getElementById(`task${taskID}`);

    const getTaskLink = (taskID) => `${taskURL}/${taskID}`;

    const queryTask = (taskID, label) => (new FormData(taskForms[taskID])).get(label);

    const refreshTask = (taskID) => {
        const taskDiv = getTaskDiv(taskID);

        fetch(getTaskLink(taskID))
                .then(response => response.text())
                .then(text => {
                    let responseDiv = document.createElement("div");
                    responseDiv.innerHTML = text;
                    taskDiv.innerHTML = responseDiv.children[0].innerHTML;

                    taskForms[taskID] = document.querySelector(`#task${taskID} form`);
                });
    };

    const pushTask = (taskID) => {
        let taskColumn = document.getElementById(`task_column`);

        fetch(getTaskLink(taskID))
                .then(response => response.text())
                .then(text => {
                    taskColumn.innerHTML += text; 

                    const form = document.querySelector(`#task${taskID} form`);
                    taskForms[taskID] = form;
                });
    };

    const initTasks = () => {
        document.addEventListener("DOMContentLoaded", () => {
            for (const taskID of taskIDs) {
                pushTask(taskID);
            }
        });
    };

    const updateTask = (taskID) => {
        // console.log(`update task called for ${taskID}`);
        const taskDiv = getTaskDiv(taskID);
        const form = document.getElementById(`form${taskID}`);
        const data = new FormData(form);
        const taskLink = getTaskLink(taskID);

        // console.log(Array.from(data));

        fetch(taskLink, { method: 'POST', body: data })
            .then(response => {
                refreshTask(taskID);
                taskIDs.filter(id => id !== taskID).forEach(id => refreshTask(id));
            });
    };

    const exported = {
        refreshTask: refreshTask,
        pushTask: pushTask,
        initTasks: initTasks, 
        updateTask: updateTask,
    };

    return exported;
};

