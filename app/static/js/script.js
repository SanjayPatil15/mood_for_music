document.getElementById('imageForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    const imageFile = document.getElementById('imageUpload').files[0];
    formData.append('image', imageFile);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display the mood result
        document.getElementById('moodResult').innerText = data.mood;

        // Clear previous song list
        const songList = document.getElementById('songList');
        songList.innerHTML = '';

        // Display the music recommendations
        data.recommendations.forEach(song => {
            const li = document.createElement('li');
            li.textContent = `${song.name} by ${song.artist} (Album: ${song.album})`;
            songList.appendChild(li);
        });

        // Show the result section
        document.getElementById('result').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
