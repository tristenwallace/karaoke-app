import { updateVideo, embedVideo } from './videoPlayer.js';

export function initializeButtonHandlers() {
    const songQueueItems = document.querySelectorAll('#songQueue .list-group-item');
    const nextSongButton = document.getElementById('nextSong');

    nextSongButton.addEventListener('click', function() {
        const currentSongItem = document.querySelector('#songQueue .list-group-item.current');
        if (currentSongItem) {
            const currentSongId = currentSongItem.dataset.id;

            fetch(`/session/${sessionCode}/next_song`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({currentSongId}),
                credentials: 'same-origin'
            }).then(response => response.json())
            .then(data => {
                console.log(`Success: ${data.success}, Message: ${data.message}`)
                if (data.success) {
                    // Remove 'current' class from the current song
                    currentSongItem.classList.remove('current');

                    // Remove the played song
                    currentSongItem.remove();
                    
                    // Update video with next song in queue
                    const nextSongItem = document.querySelector(`#songQueue .list-group-item[data-id="${data.nextSongId}"]`);
                    if (nextSongItem) {
                        nextSongItem.classList.add('current', 'bg-info', 'text-white');
                        // Update the video for the next song
                        updateVideo('#songQueue .list-group-item', embedVideo);
                    }
                } else if (data.message === 'End of queue') {
                    // Remove the queue and video player sections
                    document.getElementById('videoQueue').remove();
                    
                    // Display a nicely formatted message
                    const messageContainer = document.createElement('div');
                    messageContainer.innerHTML = `
                        <div class="alert alert-info text-center fade show" role="alert">
                            You've reached the end of the queue. Add more songs to keep the party going!
                        </div>
                    `;
                    document.querySelector('.container-fluid.pt-5').appendChild(messageContainer);
                }
            }).catch(error => {
                console.error('Fetch error:', error);
            });
        }
    });
}


export function initializeSongQueueHandlers(sessionCode) {
    let draggedItem = null;
    const songQueueList = document.getElementById('queueList');
    const songQueueItems = songQueueList.querySelectorAll('.list-group-item');

    //hover color
    songQueueList.addEventListener('mouseover', function(event) {
        if (event.target.classList.contains('list-group-item')) {
            event.target.style.background = '#f1f1f1';  // Apply hover effect
        }
    });
    
    songQueueList.addEventListener('mouseout', function(event) {
        if (event.target.classList.contains('list-group-item')) {
            event.target.style.background = '';  // Remove hover effect
        }
    });

    // Drag and Drop Handlers
    songQueueItems.forEach(item => {
        // Skip if item is not draggable
        if (item.getAttribute('draggable') === 'false') {
            return;
        }
        
        item.addEventListener('dragstart', function(e) {
            draggedItem = this;
            setTimeout(() => this.classList.add('hide'), 0);
        });

        item.addEventListener('dragend', function(e) {
            setTimeout(() => {
                draggedItem.classList.remove('hide');
                draggedItem = null;
            }, 0);
        });

        item.addEventListener('dragover', function(e) {
            e.preventDefault();
        });

        item.addEventListener('dragenter', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
            this.style.background = '#f1f1f1';
        });

        item.addEventListener('dragleave', function(e) {
            this.classList.remove('drag-over');
            this.style.background = '#ffffff';
        });

        item.addEventListener('drop', function(e) {
            this.style.background = '#ffffff';
            this.classList.remove('drag-over');
            if (this !== draggedItem) {
                // Reorder the items in the DOM
                const currentPos = Array.from(songQueueList.children).indexOf(this);
                const draggedPos = Array.from(songQueueList.children).indexOf(draggedItem);
                if (currentPos < draggedPos) {
                    songQueueList.insertBefore(draggedItem, this);
                } else {
                    songQueueList.insertBefore(draggedItem, this.nextSibling);
                }
            

                // Send the reorder request to the server
                fetch(`/session/${sessionCode}/reorder`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        draggedId: draggedItem.dataset.id,
                        targetId: this.dataset.id
                    }),
                    credentials: 'same-origin'
                }).then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                }).then(data => {
                    console.log('Reorder successful:', data);
                }).catch(error => {
                    console.error('Reorder error:', error);
                });
            }
        });
    });
}

