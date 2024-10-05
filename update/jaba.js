function showTab(tabName) {
    document.querySelector('.tab.active').classList.remove('active');
    document.querySelector('.tab-content.active').classList.remove('active');
    document.getElementById(tabName + '-tab').classList.add('active');
    document.getElementById(tabName + '-content').classList.add('active');
}
document.getElementById('groups-link').addEventListener('click', function() {
    document.querySelector('.nav-right a.active').classList.remove('active');
    this.classList.add('active');
    });

document.getElementById('home-link').addEventListener('click', function() {
    document.querySelector('.nav-right a.active').classList.remove('active');
    this.classList.add('active');
    });
const players = [];

const playersList = document.getElementById('players-list');
const noTeamsMessage = document.getElementById('no-teams-message');
if (players.length === 0) {
        playersList.style.display = 'none'; 
        noTeamsMessage.style.display = 'block'; 
} else {
    players.forEach(player => {
        const li = document.createElement('li');
        li.textContent = player;
        playersList.appendChild(li);
    });
    noTeamsMessage.style.display = 'none'; 
}

function generateGroupCode() {
    let groupCode = '';
    for (let i = 0; i < 6; i++) {
        groupCode += Math.floor(Math.random() * 10);
    }
    return groupCode;
}

document.getElementById('create-group-btn').addEventListener('click', function() {
    const groupCode = generateGroupCode();
    const groupCodeMessage = document.getElementById('group-code-message');
    groupCodeMessage.textContent = `Hey, this is your new group's code: ${groupCode}`;
});