const musicContainer = document.getElementById('music-container');
const playBtn = document.getElementById('play');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');
const audio = document.getElementById('audio');
const progress = document.getElementById('progress');
const progressContainer = document.getElementById('progress-container');
const title = document.getElementById('title');
const cover = document.getElementById('cover');
const currTime = document.querySelector('#currTime');
const durTime = document.querySelector('#durTime');
const browseButton = document.getElementById('browse');
const songList = document.getElementById('song_list');
const listenNowButton = document.getElementById('listen_now');
const browse_button = document.getElementById('browse');
const queueDisplay = document.querySelector(".queue");


let prevMood = "";

// Song titles
let songs = {};
let temp_songs = {};

// Album art
// const album_art = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19' , '20', '21']

// Play or Not
let play_song = false;

// Keep track of song
let songIndex = 0;

const moodChoice = `
				<div class="pages box">
					<div class="intro-title">Choose Mood</div>
					<div class="show" id="add_avatar">

					<form id="upload_avatar_form">
						<div class="user" style="margin: 35px; font-size: 20px;">
							<label>Choose Mood:
								<span>
									<select class="select" id="mood_choice">
										<option class="option" value="happy">Happy</option>
										<option class="option" value="sad">Sad</option>
										<option class="option" value="surprise">Surprise</option>
										<option class="option" value="angry">Angry</option>
									</select>
								</span>
							</label>
						</div>
						<div style="display: flex;margin: 10px;padding: 5px;">
							<input class="button" id="cancel_recommendation" type="submit" value="Cancel" style="display: block;margin: 15px auto 15px auto;"/>
							<input class="button" id="image_recommendation" type="submit" value="Use Image" style="display: block;margin: 15px auto 15px auto;"/>
							<input class="button" id="manual_generate" type="submit" value="Generate" style="display: block;margin: 15px auto 15px auto;"/>
					</div>
					</form>
				</div>
				`;

// Initially load song details into DOM
// loadSong(songs[songIndex]);

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

// Update song details
function loadSong(songObj) {
	// console.log(songObj);
	title.innerText = songObj.song;
	audio.src = songObj.audio_file;
	cover.src = songObj.album_art;
}

// Play song
function playSong() {

	if (songs.length > 0 && play_song){
		
		musicContainer.classList.add('play');
		playBtn.querySelector('i.fas').classList.remove('fa-play');
		playBtn.querySelector('i.fas').classList.add('fa-pause');
		audio.play();
	}
}

// Pause song
function pauseSong() {
	musicContainer.classList.remove('play');
	playBtn.querySelector('i.fas').classList.add('fa-play');
	playBtn.querySelector('i.fas').classList.remove('fa-pause');

	audio.pause();
}

// Previous song
function prevSong() {
	songIndex--;

	if (songIndex < 0) {
		songIndex = songs.length - 1;
	}

	loadSong(songs[songIndex]);

	playSong();
}

// Next song
function nextSong() {
	songIndex++;

	if (songIndex > songs.length - 1) {
		songIndex = 0;
	}

	loadSong(songs[songIndex]);

	playSong();
}

// Update progress bar
function updateProgress(e) {

	const { duration, currentTime } = e.srcElement;
	const progressPercent = (currentTime / duration) * 100;
	progress.style.width = `${progressPercent}%`;

}

// Set progress bar
function setProgress(e) {

	const width = this.clientWidth;
	const clickX = e.offsetX;
	const duration = audio.duration;
	const currentTime = (clickX / width) * duration;
	// console.log(clickX, width, duration, currentTime);a
	audio.currentTime = currentTime;
		
}

//get duration & currentTime for Time of song
function DurTime(e) {
	const { duration, currentTime } = e.srcElement;
	var sec;
	var sec_d;

	// define minutes currentTime
	let min = (currentTime == null) ? 0 :
		Math.floor(currentTime / 60);
	min = min < 10 ? '0' + min : min;

	// define seconds currentTime
	function get_sec(x) {
		if (Math.floor(x) >= 60) {

			for (var i = 1; i <= 60; i++) {
				if (Math.floor(x) >= (60 * i) && Math.floor(x) < (60 * (i + 1))) {
					sec = Math.floor(x) - (60 * i);
					sec = sec < 10 ? '0' + sec : sec;
				}
			}
		} else {
			sec = Math.floor(x);
			sec = sec < 10 ? '0' + sec : sec;
		}
	}

	get_sec(currentTime, sec);

	// change currentTime DOM
	currTime.innerHTML = min + ':' + sec;

	// define minutes duration
	let min_d = (isNaN(duration) === true) ? '0' :
		Math.floor(duration / 60);
	min_d = min_d < 10 ? '0' + min_d : min_d;


	function get_sec_d(x) {
		if (Math.floor(x) >= 60) {

			for (var i = 1; i <= 60; i++) {
				if (Math.floor(x) >= (60 * i) && Math.floor(x) < (60 * (i + 1))) {
					sec_d = Math.floor(x) - (60 * i);
					sec_d = sec_d < 10 ? '0' + sec_d : sec_d;
				}
			}
		} else {
			sec_d = (isNaN(duration) === true) ? '0' :
				Math.floor(x);
			sec_d = sec_d < 10 ? '0' + sec_d : sec_d;
		}
	}

	// define seconds duration

	get_sec_d(duration);

	// change duration DOM
	durTime.innerHTML = min_d + ':' + sec_d;

};

// Event listeners
playBtn.addEventListener('click', () => {
	const isPlaying = musicContainer.classList.contains('play');

	if (isPlaying) {
		pauseSong();
	} else {
		playSong();
	}
});

// Change song
prevBtn.addEventListener('click', prevSong);
nextBtn.addEventListener('click', nextSong);

// Time/song update
audio.addEventListener('timeupdate', updateProgress);

// Click on progress bar
progressContainer.addEventListener('click', setProgress);

// Song ends
audio.addEventListener('ended', nextSong);

// Time of song
audio.addEventListener('timeupdate', DurTime);

// Function to convert Miliseconds to Minute and Seconds
function miliToMinSec(duration) {
	var seconds = parseInt((duration/1000)%60)
	var minutes = parseInt((duration/(1000*60))%60);
	
	minutes = (minutes < 10) ? "0" + minutes : minutes;
	seconds = (seconds < 10) ? "0" + seconds : seconds;
	
	return minutes + ":" + seconds;
}


// Load the Browse Songs into the playlist Queue
function loadBrowseSongs(e) {
	songList.innerHTML = "";
	songs = temp_songs;


	for (var i in songs){
		var song_queue= `
				<li class="player__song" >
					<img class="queue_img img" src="${ songs[i].album_art }" alt="cover">
					<p class="player__context">
						  <b class="player__song-name">${ songs[i].song }</b>
						  <span class="flex">
							<span class="player__title">${ songs[i].artist }</span>
						  </span>
					</p>
			  </li>
			`;
		songList.innerHTML += song_queue;	
	};

	var Playlist = document.querySelectorAll('li');
	console.log(Playlist);

	Playlist.forEach((item, index)=>   {
		item.addEventListener("click", function() {
			loadSong(songs[index]);
			songIndex = index;
			cover.src = songs[index].album_art;
			playSong();
		});
	});

	queueDisplay.style.display = "block";				
	play_song = true;
	songIndex = 0;
	pauseSong();
	loadSong(songs[songIndex]);
	playSong();
	browseSongs();
}

// Function to Browse All Songs
function browseSongs(e) {
	
	var url = 'http://127.0.0.1:8000/display_songs';
	fetch(url)
        .then((res) => res.json())
        .then(function (data) {
            // console.log("Songs Before: ", songs);
			temp_songs = data;
			// console.log("Songs After: ", songs);
            modify_div.innerHTML = `
							<div class="table_container" style="display: none;" id="table_div">
								<table class="table">
								<thead class="thead_table">
										<tr class="tr_table">
											<th class="th_table">Song</th>
											<th class="th_table">Artist</th>
											<th class="th_table">Album</th>
											<th class="th_table">Duration</th>
										</tr>
									</thead>
									<tbody class="tbody_table" id="table_body">
									</tbody>
								</table>
							</div>
							<div style="display: flex;margin: 10px;padding: 5px;">
								<input class="button" id="play_browse" type="submit" value="Play All" style="display: block;margin: 15px auto 15px auto;"/>
							</div>
							`;
			var modify_table_row = document.getElementById('table_body');
            
			
			for (var i in data) {
				
				// songs.push(data[i].audio_file.split("/").slice(-1)[0].replace(".mp3", ""));

                var item = `
                            <tr class="tr_table">
                                <td class="td_table"> ${ temp_songs[i].song } </td>
                                <td class="td_table"> ${ temp_songs[i].artist } </td>
                                <td class="td_table"> ${ temp_songs[i].album } </td>
                                <td class="td_table"> ${ miliToMinSec(temp_songs[i].duration) } </td>
                            </tr>
                        `;
				modify_table_row.innerHTML += item;
            }
            var modify_table_div = document.getElementById('table_div');
            modify_table_div.style.display = "block"; 
			

			var playAllButton = document.querySelector('#play_browse');
			playAllButton.addEventListener('click', loadBrowseSongs);
			
        });

}


// Load the ListenNow Songs into the playlist Queue
function loadListenNowSongs(e) {
	songList.innerHTML = "";
	songs = temp_songs;
	// console.log("Songs: ", songs);
	// console.log("ListenNowSongs: ", temp_songs);

	for (var i in songs){
		var song_queue= `
				<li class="player__song" >
					<img class="queue_img img" src="${ songs[i].album_art }" alt="cover">
					<p class="player__context">
						  <b class="player__song-name">${ songs[i].song }</b>
						  <span class="flex">
							<span class="player__title">${ songs[i].artist }</span>
						  </span>
					</p>
			  </li>
			`;
		songList.innerHTML += song_queue;	
	};

	var Playlist = document.querySelectorAll('li');
	console.log(Playlist);

	Playlist.forEach((item, index)=>   {
		item.addEventListener("click", function() {
			loadSong(songs[index]);
			songIndex = index;
			cover.src = songs[index].album_art;
			playSong();
		});
	});

	queueDisplay.style.display = "block";				
	play_song = true;
	songIndex = 0;
	pauseSong();
	loadSong(songs[songIndex]);
	playSong();
	browseSongs();
}

// Function to Play Listen Now Songs
function listenNowPlay(e) {
	
	var url = 'http://127.0.0.1:8000/generate_playlist';
	fetch(url)
		.then((res) => res.json())
		.then(function (data) {

			// songList.innerHTML = "";
			temp_songs = data;

            modify_div.innerHTML = `
							<div class="table_container" style="display: none;" id="table_div">
								<table class="table">
								<thead class="thead_table">
										<tr class="tr_table">
											<th class="th_table">Song</th>
											<th class="th_table">Artist</th>
											<th class="th_table">Album</th>
											<th class="th_table">Duration</th>
										</tr>
									</thead>
									<tbody class="tbody_table" id="table_body">
									</tbody>
								</table>
							</div>
							<div style="display: flex;margin: 10px;padding: 5px;">
								<input class="button" id="cancel_recommendation" type="submit" value="Cancel" style="display: block;margin: 15px auto 15px auto;"/>
								<input class="button" id="regen_recommendation" type="submit" value="Re-Generate" style="display: block;margin: 15px auto 15px auto;"/>
								<input class="button" id="play_recommendation" type="submit" value="Play All" style="display: block;margin: 15px auto 15px auto;"/>
							</div>
							`;
			var modify_table_row = document.getElementById('table_body');
			
			for (var i in temp_songs) {
				
				var item = `
                            <tr class="tr_table">
                                <td class="td_table"> ${ temp_songs[i].song } </td>
                                <td class="td_table"> ${ temp_songs[i].artist } </td>
                                <td class="td_table"> ${ temp_songs[i].album } </td>
                                <td class="td_table"> ${ miliToMinSec(temp_songs[i].duration) } </td>
                            </tr>
                        `;
				modify_table_row.innerHTML += item;

			}

			var modify_table_div = document.getElementById('table_div');
            modify_table_div.style.display = "block"; 
			

			var ReGenButton = document.querySelector('#regen_recommendation');
			var CancelGenButton = document.querySelector('#cancel_recommendation');
			var playAllButton = document.querySelector('#play_recommendation');

			ReGenButton.addEventListener('click', listenNowPlay);
			CancelGenButton.addEventListener('click', listenNowChoice);
			playAllButton.addEventListener('click', loadListenNowSongs);
			// songIndex = 0;
		});
}

// Manual Recommendation of Songs
function manualMoodRecommend(e) {

	// console.log("Manual Mood Recommendation");
	let mood = document.getElementById('mood_choice');
	if(mood == null){
		mood = prevMood;
	}
	else{
		mood = mood.value;
		prevMood = mood;
	}

	var url = `http://127.0.0.1:8000/generate_playlist`;
	fetch(url, {
		method: "POST",
	    headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({
			'mood': mood
		})
	})
		
		.then((res) => res.json())
		.then(function (data) {

			console.log(data);
			// songList.innerHTML = "";
			temp_songs = data;

            modify_div.innerHTML = `
							<div class="table_container" style="display: none;" id="table_div">
								<table class="table">
								<thead class="thead_table">
										<tr class="tr_table">
											<th class="th_table">Song</th>
											<th class="th_table">Artist</th>
											<th class="th_table">Album</th>
											<th class="th_table">Duration</th>
										</tr>
									</thead>
									<tbody class="tbody_table" id="table_body">
									</tbody>
								</table>
							</div>
							<div style="display: flex;margin: 10px;padding: 5px;">
								<input class="button" id="cancel_recommendation" type="submit" value="Cancel" style="display: block;margin: 15px auto 15px auto;"/>
								<input class="button" id="regen_recommendation" type="submit" value="Re-Generate" style="display: block;margin: 15px auto 15px auto;"/>
								<input class="button" id="play_recommendation" type="submit" value="Play All" style="display: block;margin: 15px auto 15px auto;"/>
							</div>
							`;
			var modify_table_row = document.getElementById('table_body');
			
			for (var i in temp_songs) {
				
				var item = `
                            <tr class="tr_table">
                                <td class="td_table"> ${ temp_songs[i].song } </td>
                                <td class="td_table"> ${ temp_songs[i].artist } </td>
                                <td class="td_table"> ${ temp_songs[i].album } </td>
                                <td class="td_table"> ${ miliToMinSec(temp_songs[i].duration) } </td>
                            </tr>
                        `;
				modify_table_row.innerHTML += item;

			}

			var modify_table_div = document.getElementById('table_div');
            modify_table_div.style.display = "block"; 
			

			var ReGenButton = document.querySelector('#regen_recommendation');
			var CancelGenButton = document.querySelector('#cancel_recommendation');
			var playAllButton = document.querySelector('#play_recommendation');

			ReGenButton.addEventListener('click', manualMoodRecommend);
			CancelGenButton.addEventListener('click', listenNowChoice);
			playAllButton.addEventListener('click', loadListenNowSongs);
			// songIndex = 0;
		});
}

function listenNowChoice(e){
	
	modify_div.innerHTML = moodChoice;
	var CancelChoiceButton = document.querySelector('#cancel_recommendation');
	var UseImageGenButton = document.querySelector('#image_recommendation');
	var manualGenButton = document.querySelector('#manual_generate');

	CancelChoiceButton.addEventListener('click', browseSongs);
	UseImageGenButton.addEventListener('click', listenNowPlay);
	manualGenButton.addEventListener('click', manualMoodRecommend);
}


// Listen Now Play Songs
listenNowButton.addEventListener('click', listenNowChoice);

// Browse All Songs
browse_button.addEventListener('click', browseSongs);
browseSongs();