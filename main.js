const { app, BrowserWindow, ipcMain } = require("electron");

function createWindow() {
    const win = new BrowserWindow({
        width: 300,
        height: 300,
        frame: false,
        transparent: true,
        resizable: false,
        alwaysOnTop: true,
        hasShadow: false,

        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: __dirname + "/preload.js"
        }
    });

    win.loadFile("frontend/index.html");
   ipcMain.on("move-window", (event, { deltaX, deltaY }) => {
    const [currentX, currentY] = win.getPosition();

    win.setPosition(
        currentX + deltaX,
        currentY + deltaY
    );
});
}

app.whenReady().then(() => {
    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});