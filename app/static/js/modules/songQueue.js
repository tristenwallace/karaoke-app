import { updateVideo, embedVideo } from './videoPlayer.js';

export function initializeButtonHandlers() {
    let currentSongIndex = 0;
    const songQueueItems = document.querySelectorAll('#songQueue .list-group-item');
    const nextSongButton = document.getElementById('nextSong');

    nextSongButton.addEventListener('click', function() {
        if (currentSongIndex < songQueueItems.length - 1) {
            currentSongIndex++;
            updateVideo(currentSongIndex, '#songQueue .list-group-item', embedVideo);
        }
    });

    // Initial video embedding
    updateVideo(currentSongIndex, '#songQueue .list-group-item', embedVideo);
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
                

                // Re-bind event listeners to all list items
                rebindEventListeners();

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

