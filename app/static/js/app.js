document.addEventListener('DOMContentLoaded', function() {
    // Make an AJAX request to fetch the data from the server
    fetch('/get_names')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const tableBody = document.getElementById('tableBody');
            data.forEach(row => {
                const newRow = document.createElement('tr');
                const nameCell = document.createElement('td');
                nameCell.textContent = row[0];  // Assuming the name is in the first column
                newRow.appendChild(nameCell);
                tableBody.appendChild(newRow);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
