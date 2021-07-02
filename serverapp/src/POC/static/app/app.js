var baseUrl = "http://127.0.0.1:8000/oauth/"


var logged_in = false;
const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const logoutButton = document.getElementById("logout-button");
const loginPrmButton = document.getElementById("login-prm-button");
const accessResourceButton = document.getElementById("access-resource-button");
const usernameField = document.getElementById("username-field");
const passwordField = document.getElementById("password-field");


function adjustVisibility(flag) {
  if (flag) {
    loginButton.style.visibility = "hidden";
    usernameField.style.visibility = "hidden";
    passwordField.style.visibility = "hidden";
    logoutButton.style.visibility = "visible";
    loginPrmButton.style.visibility = "visible";
    accessResourceButton.style.visibility = "visible";
  } else {
    loginButton.style.visibility = "visible";
    usernameField.style.visibility = "visible";
    passwordField.style.visibility = "visible";
    logoutButton.style.visibility = "hidden";
    loginPrmButton.style.visibility = "hidden";
    accessResourceButton.style.visibility = "hidden";
  }
}

document.addEventListener("DOMContentLoaded", (e) => {
  adjustVisibility(logged_in);
});

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    let username = loginForm.username.value;
    let password = loginForm.password.value;
    let data = {
      "username": username,
      "password": password
    };
    fetch(baseUrl + 'login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then((response) => {
      if (response.ok)
        return response.text()
      else
        throw new Error("error");
    })
    .then((data) => {
      logged_in = true;
      adjustVisibility(logged_in);
      console.log(data);
    })
    .catch((error) => {
      console.log(error);
    });

});

logoutButton.addEventListener("click", (e) => {
  e.preventDefault();
  fetch(baseUrl + 'logout/', {
    method: 'POST'
  })
  .then((response) => {
    if (response.ok)
      return response.text()
    else
      throw new Error("error");
  })
  .then((data) => {
    logged_in = false;
    adjustVisibility(logged_in);
    console.log(data);
  })
  .catch((error) => {
    console.log(error);
  });
});

loginPrmButton.addEventListener("click", (e) => {
  e.preventDefault();
});

accessResourceButton.addEventListener("click", (e) => {
  e.preventDefault();
  fetch(baseUrl + 'prm_resource/', {
    method: 'GET'
  })
  .then(response => response.text())
  .then((data) => {
    alert(data);
  })
  .catch((error) => {
    console.log(error);
  });
})
