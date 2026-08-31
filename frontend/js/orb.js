// =========================
// ORB ELEMENTS
// =========================

const orb = document.getElementById("orb");
const backendTest = document.getElementById("backend-test");


// =========================
// DRAGGING
// =========================

let dragging = false;

let startMouseX = 0;
let startMouseY = 0;


orb.addEventListener("mousedown", (event) => {
    dragging = true;

    startMouseX = event.screenX;
    startMouseY = event.screenY;
});


document.addEventListener("mousemove", (event) => {
    if (!dragging) return;

    const deltaX =
        event.screenX - startMouseX;

    const deltaY =
        event.screenY - startMouseY;

    window.electronAPI.moveWindow(
        deltaX,
        deltaY
    );

    startMouseX = event.screenX;
    startMouseY = event.screenY;
});


document.addEventListener("mouseup", () => {
    dragging = false;
});


// =========================
// ORB STATE SYSTEM
// =========================

function setState(state) {
    orb.classList.remove(
        "idle",
        "listening",
        "thinking",
        "speaking"
    );

    orb.classList.add(state);

    console.log("Orb state:", state);
}


// =========================
// CLICK INTERACTION
// =========================

orb.addEventListener("click", async () => {

    const isListening =
        orb.classList.contains("listening");

    if (isListening) {
        return;
    }

    try {

        setState("listening");

        console.log("Listening for voice...");

        const result =
            await window.electronAPI.listen();

        setState("thinking");

        console.log(
            "Transcription:",
            result.text
        );

        alert(
            `You said:\n\n${result.text}`
        );

        setState("idle");

    } catch (error) {

        console.error(
            "Voice input failed:",
            error
        );

        setState("idle");

        alert(
            "Voice input failed. Check the backend terminal."
        );
    }

});


// =========================
// KEYBOARD TEST CONTROLS
// =========================

document.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();

    if (key === "i") {
        setState("idle");
    }

    if (key === "l") {
        setState("listening");
    }

    if (key === "t") {
        setState("thinking");
    }

    if (key === "s") {
        setState("speaking");
    }
});


// =========================
// BACKEND TEST
// =========================

backendTest.addEventListener("click", async (event) => {
    event.stopPropagation();

    try {
        const result =
            await window.electronAPI.checkBackend();

        console.log(
            "Backend response:",
            result
        );

        alert(
            "Backend connected successfully!"
        );

    } catch (error) {

        console.error(
            "Backend connection failed:",
            error
        );

        alert(
            "Backend connection failed."
        );
    }
});