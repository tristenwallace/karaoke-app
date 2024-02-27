import { initializeSongQueueHandlers, initializeButtonHandlers } from './modules/songQueue.js';

document.addEventListener('DOMContentLoaded', function () {
    initializeButtonHandlers();
    initializeSongQueueHandlers(sessionCode);
});