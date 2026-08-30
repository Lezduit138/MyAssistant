const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
    moveWindow: (deltaX, deltaY) => {
        ipcRenderer.send("move-window", { deltaX, deltaY });
    }
});