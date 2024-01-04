const searchInput = document.getElementById('search-input');

document.addEventListener('DOMContentLoaded', function() {
  
    searchInput.addEventListener('input', function() {
      const searchText = searchInput.value;
      if (searchText.length > 2) {
        fetch(`http://127.0.0.1:8000/players/search/?format=json&name=${encodeURIComponent(searchText)}`)
          .then(response => response.json())
          .then(data => {
            // TODO: process and display the data (autocomplete suggestions)
            console.log(data); // data will be an array of player names or objects
          })
          .catch(error => {
            console.error('Error fetching player data:', error);
          });
      }
    });
  
    // TODO: Add event listener for when user selects an autocomplete suggestion
    // or when the search form is submitted to fetch and display the player's statistics
  });

// Function to call the API and update the dropdown
const searchAutocomplete = async (searchTerm) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/players/search/?format=json&name=${encodeURIComponent(searchTerm)}`);
    const data = await response.json();
    // Use 'data' to populate the dropdown
    updateDropdown(data);
  } catch (error) {
    console.error('Error fetching autocomplete data:', error);
  }
};

// Event listener for the input field
searchInput.addEventListener('input', (e) => {
  const searchTerm = e.target.value;
  if (searchTerm.length > 2) { // Wait until at least 3 characters have been typed
    searchAutocomplete(searchTerm);
  }
});

// Funktion, um Spielerstatistiken zu holen und in der Konsole anzuzeigen
const fetchStatsFunction = async (playerName) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/players/search/?format=json&name=${encodeURIComponent(playerName)}`);
      const data = await response.json();
      console.log('Player statistics:', data);
    } catch (error) {
      console.error('Error fetching player statistics:', error);
    }
  };
  
  // Event listener für das Dropdown
  const updateDropdown = (suggestions) => {
      const dropdown = document.getElementById('autocomplete-results');
      dropdown.innerHTML = '';
      suggestions.forEach((item) => {
          const listItem = document.createElement('li');
          listItem.textContent = item.player_Name;
          listItem.addEventListener('click', () => {
              searchInput.value = item.player_Name;
              fetchStatsFunction(item.player_Name); // Ruft Statistiken des ausgewählten Spielers ab
          });
          dropdown.appendChild(listItem);
      });
  };
