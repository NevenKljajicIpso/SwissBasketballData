const searchInput = document.getElementById('search-input');

const playerNameHtml = document.querySelector('.player-name');
const playerClubHtml = document.querySelector('.player-club');

document.addEventListener('DOMContentLoaded', function() {
    searchInput.addEventListener('input', function() {
        const searchText = searchInput.value;
        if (searchText.length > 2) {
            searchAutocomplete(searchText);
        } else {
            dropdown.innerHTML = ''; // Leert das Dropdown, wenn das Eingabefeld leer ist oder weniger als drei Zeichen enthält
        }
    });
});

// Function to call the API and update the dropdown
const searchAutocomplete = async (searchTerm) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/players/search/?format=json&name=${encodeURIComponent(searchTerm)}`);
    const data = await response.json();
    updateDropdown(data);
  } catch (error) {
    console.error('Error fetching autocomplete data:', error);
  }
};

// Funktion, um Spielerstatistiken zu holen und in der Konsole anzuzeigen
const fetchStatsFunction = async (playerName) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/players/search/?format=json&name=${encodeURIComponent(playerName)}`);
      const data = await response.json();
      console.log('Player statistics:', data[0]);

      displayData(data);

      //playerNameHtml.textContent = data[0].player_Name;
      //playerClubHtml.textContent = data[0].teams[0];

    } catch (error) {
      console.error('Error fetching player statistics:', error);
    }
};
  
const updateDropdown = (suggestions) => {
    const dropdown = document.getElementById('autocomplete-results');
    dropdown.innerHTML = ''; // Leert das Dropdown vor dem Hinzufügen neuer Elemente
    suggestions.forEach((item) => {
        const listItem = document.createElement('li');
        listItem.textContent = item.player_Name;
        listItem.addEventListener('click', () => {
            searchInput.value = item.player_Name;
            fetchStatsFunction(item.player_Name); // Ruft Statistiken des ausgewählten Spielers ab
            dropdown.innerHTML = ''; // Leert das Dropdown, wenn ein Spieler ausgewählt wird
        });
        dropdown.appendChild(listItem);
    });
};


const displayData = (stats) => {
    playerNameHtml.textContent = data[0].player_Name;
    playerClubHtml.textContent = data[0].teams[0];
}