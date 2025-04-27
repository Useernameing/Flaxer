function startCapture() {
    fetch('http://localhost:5000/start')
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error('Hata:', error);
        });
}

function stopCapture() {
    fetch('http://localhost:5000/stop')
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error('Hata:', error);
        });
}
