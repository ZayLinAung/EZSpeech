let intervalId = null;

const updateListeningText = () => {
    fetch("/static/data/dummy_data.txt") // Adjust the path as needed
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then(text => {
        document.getElementById('listening').innerText = text;
      })
      .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
      });
}

// const updateResponsesText = () => {
//   fetch("backend/outprompts.txt") // Adjust the path as needed
//     .then(response => {
//       if (!response.ok) {
//         throw new Error('Network response was not ok');
//       }
//       return response.text();
//     })
//     .then(text => {
//       document.getElementById('responses').innerText = text;
//     })
//     .catch(error => {
//       console.error('There was a problem with your fetch operation:', error);
//     });
// }

// updateListeningText();
// intervalId = setInterval(updateListeningText, 5000);

document.getElementById('startButton').addEventListener('click', () => {
    fetch("http://127.0.0.1:5000/transcribe/en")
    console.log("HERE!")
    updateListeningText()
    if (intervalId === null) {
      //console.log("HERE!")
      updateListeningText();
      intervalId = setInterval(updateListeningText, 5000);
      
    }
});

document.getElementById('stopButton').addEventListener('click', () => {
    if (intervalId !== null) {
      clearInterval(intervalId);
      intervalId = null;
      document.getElementById('listening').innerText = "";
    }
});

