const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {

    moveWindow: (deltaX, deltaY) => {
        ipcRenderer.send("move-window", {
            deltaX,
            deltaY
        });
    },

    checkBackend: async () => {

        const response =
            await fetch(
                "http://127.0.0.1:8765/health"
            );

        if (!response.ok) {
            throw new Error(
                `Backend returned ${response.status}`
            );
        }

        return response.json();
    },

    listen: async () => {

        const response =
            await fetch(
                "http://127.0.0.1:8765/listen",
                {
                    method: "POST"
                }
            );

        if (!response.ok) {
            const error =
                await response.text();

            throw new Error(error);
        }

        return response.json();
    }

});