// function validateSignupForm() {
//     var username = document.getElementById("username").value;
//     var email = document.getElementById("email").value;
//     var password = document.getElementById("password").value;

//     // Check if all fields are required
//     if (username === "" || email === "" || password === "") {
//         alert("All fields are required!");
//         return false;
//     }

//     // Validate the username and email addresses
//     var regex = new RegExp("^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$");
//     if (!regex.test(email)) {
//         alert("Invalid email address!");
//         return false;
//     }

//     // Validate the password length
//     if (password.length < 8) {
//         alert("Password must be at least 8 characters long!");
//         return false;
//     }

//     // All fields are valid!
//     return true;
// }

// // Validate the log in form
// function validateLoginForm() {
//     var username = document.getElementById("username").value;
//     var password = document.getElementById("password").value;

//     // Check if all fields are required
//     if (username === "" || password === "") {
//         alert("All fields are required!");
//         return false;
//     }

//     // All fields are valid!
//     return true;
// }























// document.addEventListener('DOMContentLoaded', function() {
//     // Make an AJAX request to fetch the data from the server
//     fetch('/get_names')
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);
//             const tableBody = document.getElementById('tableBody');
//             data.forEach(row => {
//                 const newRow = document.createElement('tr');
//                 const nameCell = document.createElement('td');
//                 nameCell.textContent = row[0];  // Assuming the name is in the first column
//                 newRow.appendChild(nameCell);
//                 tableBody.appendChild(newRow);
//             });
//         })
//         .catch(error => {
//             console.error('Error fetching data:', error);
//         });
// });
