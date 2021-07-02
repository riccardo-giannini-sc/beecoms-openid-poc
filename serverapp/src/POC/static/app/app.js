var baseUrl = "http://127.0.0.1:8000/oauth/"
var prmUrl = "http://127.0.0.1:8002/o/authorize"
var redirect_uri = 'http://127.0.0.1:8000';

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
  fetch(baseUrl + 'session/')
  .then(response => {
    if (response.ok) {
      logged_in = true;
      adjustVisibility(logged_in);
      let urlParams = new URLSearchParams(window.location.search);
      let code = urlParams.get('code');
      if (code) {
        console.log("CODE ->", code);
        let data = {
          "code": code,
          "redirect_uri": redirect_uri
        }
        fetch(baseUrl + 'authcode/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        })
        .then(response => {
          let res_ok = false;
          if (response.ok) {
            res_ok = true;
          }
          return response.text();
        })
        .then(data => alert(data))
        .catch(error => console.log(error))

      }
    }
    else {
      logged_in = false;
      adjustVisibility(logged_in);
    }
  });

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
  fetch(baseUrl + 'client_id/')
  .then(response => response.text())
  .then((data) => {
    let client_id = data;
    console.log(data);
    // window.open(prmUrl + '?response_type=code' +
    //                                 '&client_id=' + client_id +
    //                                 '&redirect_uri=' + redirect_uri)
    window.location.href = prmUrl + '?response_type=code' +
                                    '&client_id=' + client_id +
                                    '&redirect_uri=' + redirect_uri
  })
  .catch((error) => {
    console.log(error);
  });
});



accessResourceButton.addEventListener("click", (e) => {
  e.preventDefault();
  fetch(baseUrl + 'prm_resource/')
  .then(response => response.text())
  .then((data) => {
    alert(data);
  })
  .catch((error) => {
    console.log(error);
  });
})
