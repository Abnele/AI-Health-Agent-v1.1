


window.onload = async () => {
    // Default to today's date
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    document.getElementById('data-date').value = `${yyyy}-${mm}-${dd}`;

    // Load previous data
    const res = await fetch('/goals')
    const goals = await res.json()
    
    
    if (goals.steps)        document.getElementById('goal-steps').value = goals.steps
    if (goals.hours_slept)  document.getElementById('goal-sleep').value = goals.hours_slept
    if (goals.screen_time)  document.getElementById('goal-screen').value = goals.screen_time

    // Check for exports
    const eventSource = new EventSource('/stream');

    eventSource.onmessage = async (event) => {
        const message = JSON.parse(event.data)
        console.log(message.event);
        
        if (message.event === 'export_received') {
            await refreshHistory();
            alert("Data has been exported. Manyally add screen time and edit sleep data if none was provided by your iphone")
        }
    

    };

    eventSource.onerror = () => {
        console.log('SSE connection lost connection, will retry automatically...');
    };

    

}

async function saveGoals() {
    const goals = {
        steps:          parseInt(document.getElementById('goal-steps').value),
        hours_slept:    parseInt(document.getElementById('goal-sleep').value),
        screen_time:    parseInt(document.getElementById('goal-screen').value)

    };

    const res = await fetch('/goals', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(goals)
    });
    if (res.ok) alert('Goals saved!')
}

async function addData() {
    const data_today = {
        date:           document.getElementById('data-date').value,
        steps:          parseInt(document.getElementById('data-steps').value),
        hours_slept:    parseInt(document.getElementById('data-sleep').value),
        screen_time:    parseInt(document.getElementById('data-screen').value)

    };

    let null_response = false;
    for (entry of Object.values(data_today)) {
        console.log(entry);
        if (!entry) {
            null_response = true;
        }

    };

    if (null_response) {
        alert('Please enter valid data');
        return; 
    }
    
    const checkDateRes = await fetch(`/check-date?date=${data_today.date}`)
    const checkDate = await checkDateRes.json();

    if (checkDate.exists) {
        const confirmOverride = confirm(`You already have data for ${data_today.date}. Override it?`)
        if (!confirmOverride) return;
    }
    
    
    const res = await fetch('/data', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data_today)
    });
    if (res.ok) alert('Data added!') 
    
    refreshHistory();
    
    
}


async function getAdvice() {

    const goalsRes = await fetch('/goals')
    goals = await goalsRes.json();

    const dataRes = await fetch('/history')
    data = await dataRes.json();

    let problems = []
    if (Object.keys(goals).length === 0) problems.push('GOALS')
    if (Object.keys(data).length === 0) problems.push('DATA')
    
    if (problems.length > 0){
        document.getElementById('report-type').textContent = 'ERRONEOUS REPORT';
        const list = document.getElementById('advice-list');
        list.innerHTML = '';
        const li = document.createElement('li');
        li.textContent = ("Missing: " + problems.join(", ") + ". Please add this before generating a report.");
        list.appendChild(li)
    }
    else{
        const res = await fetch('/advice');
        const adviceData = await res.json();

        document.getElementById('report-type').textContent = adviceData.report_type + ' REPORT';
        const list = document.getElementById('advice-list');
        list.innerHTML = '';

        for (const item of adviceData.advice) {
            const li = document.createElement('li')
            li.textContent = item;
            list.appendChild(li);
    }
    }
    

}

async function refreshHistory() {
    const dataRes = await fetch('/history');
    data = await dataRes.json();

    const container = document.getElementById('logged-days');
    container.innerHTML = '';

    // Sort from newest to oldest
    data.sort((a, b) => b.date.localeCompare(a.date));

    for (const entry of data){
        const day = document.createElement('div');
        day.id = `data-card-${entry.date}`;
        day.className = "data-card";
        day.innerHTML =`

        <Strong>${entry.date}</Strong>
        <p id = "card-steps-${entry.date}"  >   Steps:           ${entry.steps}<p>
        <p id = "card-sleep-${entry.date}"  >   Hours Slept:     ${entry.hours_slept}<p>
        <p id = "card-screen-${entry.date}" >   Screen time:    ${entry.screen_time}<p>
        <button onclick = "editDay('${entry.date}')">  Edit    </button>
        <button onclick = "deleteDay('${entry.date}')">        Delete  </button>
        `

        container.appendChild(day);
    }

}

async function editDay(date) {
    const historyRes = await fetch('/history')
    const history = await historyRes.json();
    const entry = history.find(e => e.date === date);

    day = document.getElementById(`data-card-${date}`);
    day.innerHTML = `

        <Strong>${date}</Strong>
        <p>Steps:           <input type = "number" value = "${entry.steps}" id = "edit-steps-${entry.date}"> <p>
        <p>Hours Slept:     <input type = "number" value = "${entry.hours_slept}" id = "edit-sleep-${entry.date}"><p>
        <p>Screen time:     <input type = "number" value = "${entry.screen_time}" id = "edit-screen-${entry.date}"><p>
        <button onClick = "confirmEdit('${date}')">Confirm</button> 
        <button onclick = "undoEdit('${date}')">Cancel</button>
    `
}

async function confirmEdit(date){
    const historyRes = await fetch('/history')
    const history = await historyRes.json();
    const entry = history.find(e => e.date === date);

    day = document.getElementById(`data-card-${date}`);
    updates = {
        "date":         date,
        "steps":        parseInt(document.getElementById(`edit-steps-${date}`).value),
        "hours_slept":  parseInt(document.getElementById(`edit-sleep-${date}`).value),
        "screen_time":  parseInt(document.getElementById(`edit-screen-${date}`).value),
    };

    const dataRes = await fetch('/data', {
        method:     'POST',
        headers:    {'Content-type': 'application/json'},
        body:       JSON.stringify(updates)        
    });
    if (dataRes.ok) alert('Data Updated!');

    refreshHistory();
}

async function undoEdit(date){
    const historyRes = await fetch('/history');
    const history = await historyRes.json();
    const entry = history.find(e => e.date === date);

    day = document.getElementById(`data-card-${date}`);
    day.innerHTML = `
        <Strong>${date}</Strong>
        <p id = "card-steps-${date}"  >   Steps:           ${entry.steps}<p>
        <p id = "card-sleep-${date}"  >   Hours Slept:     ${entry.hours_slept}<p>
        <p id = "card-screen-${date}" >   Screen time:    ${entry.screen_time}<p>
        <button onclick = "editDay('${date}')">Edit</button>
        <button onclick = "deleteDay('${date}')">Delete</button>
    `    
}

async function deleteDay(date) {
    const confirmDeletion = confirm('Delete this entry?');
    if (!confirmDeletion) {
        return;
    }
    const deleteRes = await fetch(`/data/${date}`, {method : 'DELETE'});
    if (deleteRes.ok) alert('Day Deleted!');
    refreshHistory();
}

async function resetExportAlert() {

    // Yo bro you need to read alert.json and overwrite it to false using JS
    // That's what this function should do
    // Idk if the alert_file parameter is needed
    // Put it there just in case
    // Nvm not needed
    
    const alertRes = await fetch('/communications');
    const alert = await alertRes.json();

    await fetch('/communications', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"auto_export_data_added?": false})
    })



}