
document.addEventListener("DOMContentLoaded", () => {
    let darkModeButton = document.getElementById('dark-mode-toggle');
    let section = document.querySelector('section.hero');

    const oldColor = "#00d1b2";
    const newColor = "#363636";

    const oldLabel = "Dark Mode";
    const newLabel = "Light Mode";

    let inDarkMode = false;

    darkModeButton.addEventListener('click', () => {

        if (!inDarkMode) {
            section.style.backgroundColor = newColor;
            darkModeButton.innerHTML = newLabel;
            inDarkMode = true;
        } else {
            section.style.backgroundColor = oldColor;
            darkModeButton.innerHTML = oldLabel;
            inDarkMode = false;
        }
    });
});
