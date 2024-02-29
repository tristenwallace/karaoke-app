import { initializeSongQueueHandlers, initializeButtonHandlers } from './modules/songQueue.js';
import { updateVideo, embedVideo } from './modules/videoPlayer.js';

document.addEventListener('DOMContentLoaded', function () {
    // Initial video embedding
    updateVideo('#songQueue .list-group-item', embedVideo);
    
    initializeButtonHandlers();
    initializeSongQueueHandlers(sessionCode);

    // Close alerts with a fade effect after 3 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert:not(#videoContainer .alert)');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert); // Initialize the Bootstrap alert
            bsAlert.close(); // This will close the alert with Bootstrap's built-in fade effect
        });
    }, 5000);
});