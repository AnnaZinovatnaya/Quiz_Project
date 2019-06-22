let logoutBtn = document.getElementById('logoutButton');
logoutBtn.addEventListener('mouseenter', something);
logoutBtn.addEventListener('mouseout', something2);

function something() {
    this.innerHTML = "LOGOUT";
}

function something2() {
    this.innerHTML = "Logout";
}