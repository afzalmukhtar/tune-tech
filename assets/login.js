const sign_up = document.querySelector("#sign_up");
const sign_in = document.querySelector("#sign_in");
const usn_sign_up = document.querySelector("#usn_sign_up");
const email_sign_up = document.querySelector("#email_sign_up");
const password_sign_up = document.querySelector("#password_sign_up");
const email_sign_in = document.querySelector("#email_sign_in");
const password_sign_in = document.querySelector("#password_sign_in");
const sign_in_info = document.querySelector("#sign_in_info");
const sign_up_info = document.querySelector("#sign_up_info");

const signInBtn = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUp");
const container = document.querySelector(".container");


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


signInBtn.addEventListener("click", () => {
	container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
	container.classList.add("right-panel-active");
});


// Check and Signup
function signUpCheck(e) {
    e.preventDefault();
    var usn = usn_sign_up.value;
    var email = email_sign_up.value;
    var password = password_sign_up.value;

    fetch('http://127.0.0.1:8000/signup_check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body: JSON.stringify({
            "username": usn,
            "email": email,
            "password": password
        })
    }).then( response => response.json()
    ).then(data => {
        sign_up_info.innerText = data;
        sign_up_info.style.display = "block";
        sign_in_info.style.display = "none";
        if(data.toLowerCase().includes("successful")){
            sign_up_info.style.color = "#3c763d";
            sign_up_info.style.backgroundColor = "#dff0d8";
        }
        else{
            sign_up_info.style.color = "#D8000C";
            sign_up_info.style.backgroundColor = "#FFBABA";
        }
        
    }).catch((error) => {
        console.error('Error:', error);
    });
}

// Check and Login
function logInCheck(e) {
    e.preventDefault();
    var email = email_sign_in.value;
    var password = password_sign_in.value;

    fetch('http://127.0.0.1:8000/login_check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body: JSON.stringify({
            "email": email,
            "password": password
        })
    }).then( response => response.json()
    ).then(data => {
        // console.log(data['message'])
        if(data['message'].toLowerCase().includes("successful")){
            location.href = `http://localhost:8000/dashboard/${data['username']}`;
        }
        else{
            sign_in_info.innerText = data['message'];
            sign_in_info.style.display = "block";
            sign_up_info.style.display = "none";
            sign_in_info.style.color = "#D8000C";
            sign_in_info.style.backgroundColor = "#FFBABA";
        }
    }).catch((error) => {
        console.error('Error:', error);
    });
}

// Event Listeners
sign_up.addEventListener('submit', signUpCheck);
sign_in.addEventListener('submit', logInCheck);


// document.getElementById('login_form').addEventListener('submit', function(event) {
//     event.preventDefault();
//     let email = document.getElementById('id_email').value;
//     let password = document.getElementById('id_password').value;

//     fetch('http://127.0.0.1:8000/test', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken' : csrftoken,
//         },
//         body: JSON.stringify({
//             "username": email,
//             "password": password,
//         })
//     }).then( response => {
//         return response.json();
//     }).then(data => {
//         console.log(data);
//         userToken = data.token;
//         console.log('Logged in. Got the token.');
//     }).catch((error) => {
//         console.error('Error:', error);
//     });
// });

// document.getElementById('avatar_form').addEventListener('submit', function(event) {
//     event.preventDefault();
//     let input = document.getElementById('id_avatar');

//     let data = new FormData();
//     data.append('file', input.files[0]);

//     fetch('http://127.0.0.1:8000/test', {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken' : csrftoken,
//         },
//         body: data
//     }).then(response => {
//         return response.json();
//     }).then(data => {
//         console.log(data);
//     }).catch((error) => {
//         console.error('Error:', error);
//     });
// });