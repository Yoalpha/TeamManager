console.log("JavaScript file loaded successfully!");
function generateBracket() {
    console.log("JavaScript file loaded successfully!");
    const bracket = document.getElementById('bracket');
    bracket.innerHTML = '';
    //got to fetch the datat here and get it into teams and the other arrays
    const teams = [
        'Team 1', 'Team 2', 'Team 3', 'Team 4',
        'Team 5', 'Team 6','Team 7'
    ];
    let numRounds = Math.ceil(Math.log2(teams.length));
    const matchesPerRound = [];
    let currentRoundTeams = [...teams];
    for (let round = 0; round < numRounds; round++) {
        let matches = [];
        for (let i = 0; i < currentRoundTeams.length; i += 2) {
            if (i + 1 < currentRoundTeams.length) {
                matches.push({ team1: currentRoundTeams[i], team2: currentRoundTeams[i + 1], winner: '' });
            } else {
                matches.push({ team1: currentRoundTeams[i], team2: '(bye)', winner: currentRoundTeams[i] });
            }
        }
        matchesPerRound.push(matches);
        currentRoundTeams = matches.map(() => '');
    }

    let winnersByRound = []; // this is for storing all of the winners

    function handleWinnerEntry(input, roundIndex, matchIndex) {
        const winner = input.value.trim();
        const match = matchesPerRound[roundIndex][matchIndex];
        if (winner !== match.team1 && winner !== match.team2) {
            alert(`Invalid winner! Please enter either "${match.team1}" or "${match.team2}".`);
            input.value = ''; 
            input.focus(); 
        }
    
        if (!winnersByRound[roundIndex]) {
            winnersByRound[roundIndex] = [];
        }
        winnersByRound[roundIndex][matchIndex] = winner;
        if (roundIndex + 1 < matchesPerRound.length) {
            const nextRoundMatchIndex = Math.floor(matchIndex / 2);
            const nextRoundTeamPosition = matchIndex % 2 === 0 ? 'team1' : 'team2';
            const nextRoundMatchDiv = document.getElementById(`round-${roundIndex + 1}-match-${nextRoundMatchIndex}`);
            const nextRoundTeamSpan = nextRoundMatchDiv.querySelector(`.${nextRoundTeamPosition}`);
            nextRoundTeamSpan.innerText = winner;
            matchesPerRound[roundIndex + 1][nextRoundMatchIndex][nextRoundTeamPosition] = winner;
        } else {
            document.getElementById('final-winner').innerText = `Winner: ${winner}`;
        }
  
        input.remove();
    }

    matchesPerRound.forEach((matches, roundIndex) => {
        const roundDiv = document.createElement('div');
        roundDiv.classList.add('round');
        matches.forEach((match, matchIndex) => {
            const matchDiv = document.createElement('div');
            matchDiv.classList.add('match');
            matchDiv.id = `round-${roundIndex}-match-${matchIndex}`;
            matchDiv.innerHTML = `
                <span class="team1">${match.team1 || ''}</span>
                <span class="vs"> vs </span>
                <span class="team2">${match.team2 || ''}</span>
            `;
            matchDiv.addEventListener('click', () => {
                if (!matchDiv.querySelector('.team-input')) {
                    const teamInput = document.createElement('input');
                    teamInput.type = 'text';
                    teamInput.placeholder = 'Enter Winner';
                    teamInput.classList.add('team-input');
                    teamInput.addEventListener('keydown', (event) => {
                        if (event.key === 'Enter') {
                            handleWinnerEntry(teamInput, roundIndex, matchIndex);
                        }
                    });
                    matchDiv.appendChild(teamInput);
                    teamInput.focus();
                }
            });
            const connector = document.createElement('div');
            connector.classList.add('connector');
            matchDiv.appendChild(connector);
            if (match.team2 === '(bye)' || (matchIndex === matches.length - 1 && matches.length % 2 !== 0)) {
                connector.style.width = '50px';
            } else {
                if (matchIndex % 2 === 0) {
                    const connectorDown = document.createElement('div');
                    connectorDown.classList.add('connector-down');
                    matchDiv.appendChild(connectorDown);
                } else {
                    const connectorUp = document.createElement('div');
                    connectorUp.classList.add('connector-up');
                    matchDiv.appendChild(connectorUp);
                }
            }
            roundDiv.appendChild(matchDiv);
        });
        bracket.appendChild(roundDiv);
    });

    const finalWinnerDiv = document.createElement('div');
    finalWinnerDiv.id = 'final-winner';
    finalWinnerDiv.classList.add('final-winner');
    finalWinnerDiv.innerText = 'Winner: ';
    bracket.appendChild(finalWinnerDiv);
}


document.addEventListener('DOMContentLoaded', () => {
    generateBracket();
});
console.log("JavaScript file loaded successfully!");

