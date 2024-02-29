export function embedVideo(videoLink, isEmbeddable, thumbnailUrl, containerSelector) {
    const videoContainer = document.querySelector(containerSelector);
    // if (isEmbeddable) {
    //    videoContainer.innerHTML = `<iframe class="embed-responsive-item" src="${videoLink.replace('watch?v=', 'embed/')}" allowfullscreen></iframe>`;
    //} else {
        videoContainer.innerHTML = `
            <img src="${thumbnailUrl}" class="embed-responsive-item" alt="Video Thumbnail">
            <div class="alert alert-info mt-2">This video is not available for embedding. <a href="${videoLink}" target="_blank">Watch on YouTube</a></div>
        `;
    //}
}

export function updateVideo(songQueueSelector, updateFunction=embedVideo) {
    // Find the current song item by its class
    const currentSongItem = document.querySelector(`${songQueueSelector}.current`);

    if (currentSongItem) {
        const videoLink = currentSongItem.getAttribute('data-video-link');
        const isEmbeddable = currentSongItem.getAttribute('data-is-embeddable') === 'True';
        const thumbnailUrl = currentSongItem.getAttribute('data-video-thumbnail');
        console.log(videoLink, isEmbeddable, thumbnailUrl);
        updateFunction(videoLink, isEmbeddable, thumbnailUrl, '#videoContainer');
    }
}