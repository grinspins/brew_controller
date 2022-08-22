const URL = "http://localhost:8000/controller/state"

const updateState = () => {
  fetch(URL).then((response) => response.json())
  .then((data) => {
    const div = document.getElementById("test")
    div.innerText = JSON.stringify(data);
  });
}

setInterval(updateState, 5000);



