const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
    moveWindow: (deltaX, deltaY) => {
        ipcRenderer.send("move-window", { deltaX, deltaY });
    },

    checkBackend: async () => {
        const response = await fetch("http://127.0.0.1:8765/health");

        if (!response.ok) {
            throw new Error(`Backend returned ${response.status}`);
        }

        return response.json();
    }
});