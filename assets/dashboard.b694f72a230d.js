// All Functions and Event Listeners for Dashboard functions

const add_songs_button = document.querySelector('#add_songs');
const modify_div = document.querySelector('#modify_div');
const logout_button = document.querySelector('#logout');
const currentUser = document.querySelector('#currentUser').innerText;
const profile_image = document.querySelector('#profile_image');
const profile_image_small = document.querySelector('#profile_image_small');


const add_song_html = `
                        <div class="pages box">
                            <div class="intro-title">Add Songs</div>
                            <div class="show" id="add_songs_div">
                            
                            <!-- Upload Song Data Form -->
                            <form id="add_songs_form">
                                <div class="user" style="margin: 35px; font-size: 20px;">
                                    <span>Song Name: </span>
                                    <span><input required id="song_name" type="text" placeholder="Song Name"></span>
                                </div>
                                <div class="user" style="margin: 35px; font-size: 20px;">
                                    <span>Artist Name: </span>
                                    <span><input required id="artist_name" type="text" placeholder="Artist Name"></span>
                                </div>
                                <div>
                                    <input class="button" type="submit" value="Submit" style="margin: 15px 35px;"/>
                                </div>
                            </form>

                            <!-- Upload Song Form -->
                            <form id="upload_song_form">
                                <div class="user" style="margin: 35px; font-size: 20px;">
                                    <label>Choose File:
                                        <span class="button"><input id="audio_file" required="" type="file"></span>
                                    </label>
                                </div>
                                <div class="user" style="margin: 35px; font-size: 20px;">
                                    <input id="uploadFile" placeholder="No File" disabled="disabled" />
                                </div>
                                <div>
                                    <input class="button" type="submit" value="Submit File" style="margin: 15px 35px;"/>
                                </div>
                            </form>
                        </div>
                        `;

const change_image = `
                        <div class="pages box">
                            <div class="intro-title">Choose Image</div>
                            <div class="show" id="add_avatar">

                            <form id="upload_avatar_form">
                                <div class="user" style="margin: 35px; font-size: 20px;">
                                    <label>Choose File:
                                        <span class="button"><input id="image_file" required="" type="file"></span>
                                    </label>
                                </div>
                                <div class="user" style="margin: 35px; font-size: 20px;">
                                    <input id="uploadFile" placeholder="No File" disabled="disabled" />
                                </div>
                                <div>
                                    <input class="button" type="submit" value="Submit File" style="margin: 15px 35px;"/>
                                </div>
                            </form>
                        </div>
                        `;



// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// const csrftoken = getCookie('csrftoken');


function addSongInfo(e){
    modify_div.innerHTML = add_song_html;
    const upload_song_form = document.querySelector("#upload_song_form");
    upload_song_form.style.display = "none";
    var form_element = document.querySelector('#add_songs_form');
    form_element.addEventListener('submit', function (e) {
        e.preventDefault();
        // console.log('FORM DATA SUBMITTED LOGGING TEST');
        var url_details = 'http://127.0.0.1:8000/add_song_info';
        var song_title = document.querySelector('#song_name').value;
        var artist_name = document.querySelector('#artist_name').value;
        fetch(url_details, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'song': song_title,
                'artist': artist_name,
            })
        }).then(function (response) {
            // console.log(response.json());

            upload_song_form.style.display = "block";
            const upload_name = document.querySelector("#uploadFile");

            audio_file.onchange = function () {
                upload_name.value = audio_file.files[0].name;
            };

            upload_song_form.addEventListener('submit', function (e) {
                e.preventDefault();

                var url_upload = 'http://127.0.0.1:8000/upload_song';
                const audio_file = document.querySelector('#audio_file');
                let data = new FormData();
                data.append('audio_file', audio_file.files[0]);
                // console.log(audio_file.files);

                fetch(url_upload, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    body: data

                }).then((response) => response.json())
                }).then((data) => {
                    console.log(data);
                }).catch((error) => {
                    console.error('Error: ', error);
                });

            addSongInfo();
        });
    });
}

function logout(e){
    fetch('http://localhost:8000/logout', {
        method: "GET",
        redirect: "follow"
    })
    .then(data => {
        // console.log(data['message']);
        location.href = 'http://127.0.0.1:8000/';
    })
}


function changeProfileImage(e){
    // console.log('Change Profile Button');
    modify_div.innerHTML = change_image;
    const upload_avatar_form = document.querySelector("#upload_avatar_form");
    const upload_name = document.querySelector("#uploadFile");
    // const image_file = document.getElementById('image_file');
    image_file.onchange = function () {
        upload_name.value = image_file.files[0].name;
    };

    upload_avatar_form.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log("Avatar Uploading");
        var url_upload_image = `http://127.0.0.1:8000/upload_avatar/${currentUser}`;
        // var url_upload_image = `http://127.0.0.1:8000/upload_avatar`;
        const image = document.querySelector('#image_file');
        let data = new FormData();
        data.append('image', image.files[0]);

        fetch(url_upload_image, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: data
        })
        .then((response) => response.json())
        .then(data => {
            console.log(data['message']);
            if(data['message'].toLowerCase().includes("successfully")){
                profile_image.src = data['image'];
                profile_image_small.src = data['image'];
            }
        }).catch((error) => {
            console.error('Error: ', error);
        });
    });
}

profile_image.addEventListener('click', changeProfileImage);
add_songs_button.addEventListener('click', addSongInfo);
logout_button.addEventListener('click', logout);
