let videoId = "";
let baseURL = "http://localhost:5000/api/videos/";

function prettyConvert(seconds){

  seconds = parseInt(seconds,10)

  var res = new Date(seconds*1000).toISOString().substring(11,16);
  if (seconds<3600){
    res = new Date(seconds*1000).toISOString().substring(14,19);
  }
  return res;

}

function updateVideoId (){
  chrome.tabs.query(
    { active: true, windowId: chrome.windows.WINDOW_ID_CURRENT },
    function (tabs) {
      var x = String(tabs[0].url);
      x = x.substring(32);
      videoId = x;
    }
  );
}

function getData() {
  var reqURL = baseURL + videoId;

  fetch(reqURL)
    .then((res) => res.json())
    .then((data) => {
      var afterIntro = data["afterIntro"]
      var beforeIntro = data["beforeIntro"]

      document.getElementById("startTime").innerHTML = "Starts at "+ prettyConvert(beforeIntro);
      document.getElementById("endTime").innerHTML = "Ends at " + prettyConvert(afterIntro);
    });
}

// hello world!

function postData(){

    let startTime = document.getElementById("startTimeField").value;
    let endTime = document.getElementById("endTimeField").value;

    var reqURL = baseURL + videoId;

    fetch(reqURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        afterIntro: endTime,
        beforeIntro: startTime,
      })
    })
      .then((res) => {
        if (res.ok) {
          console.log("POST Request Successful");
        } else {
          console.log("POST Request Not successful");
        }
      })
      // should return the data that was passed into the post request
      .then((data) => console.log(data));
    
    alert("Your data has been sent!")
}
document.getElementById("submitBtn").onclick = function () {
  updateVideoId();
  postData();
};
// Opens field forms
document.getElementById("openBtn").onclick = function () {
  document.getElementById("myForm").style.display = "block";
};

// Closes field forms
document.getElementById("closeBtn").onclick = function () {
  document.getElementById("myForm").style.display = "none";
};

document.getElementById("getDataBtn").onclick = function(){
  updateVideoId();
  getData();
}

function noData() {
  document.getElementById("introductionTitle").innerHTML =
    "No data avaliable. Add a new time by clicking the edit button below.";
  document.getElementById("sponsorTitle").innerHTML =
    "No data avaliable. Add a new time by clicking the edit button below.";
}