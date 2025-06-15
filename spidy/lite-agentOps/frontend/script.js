let taskCount = 0;

function addTask() {
    const div = document.createElement('div');
    div.innerHTML = `
        Task ${taskCount + 1}: 
        <input type="text" placeholder="Shell Command" id="task-${taskCount}">
        <br><br>
    `;
    document.getElementById('tasks').appendChild(div);
    taskCount++;
}

async function runWorkflow() {
    const name = document.getElementById('workflowName').value;
    const tasks = [];

    for (let i = 0; i < taskCount; i++) {
        const command = document.getElementById(`task-${i}`).value;
        if (command.trim() !== "") {
            tasks.push({ type: "shell", command });
        }
    }

    const response = await fetch("http://localhost:8000/run-workflow", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, tasks })
    });

    const result = await response.json();
    document.getElementById("output").textContent = JSON.stringify(result, null, 2);
}
