const themeToggle = document.querySelector('#theme-toggle');
const page = document.documentElement;

themeToggle.addEventListener("click", function() {
    const nextTheme = 
        page.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
    localStorage.setItem("theme", nextTheme);
});

function applyTheme(theme) {
    const isDark = theme === "dark";

    page.dataset.theme = theme;
    themeToggle.textContent = isDark ? "Light mode" : "Dark mode";
    themeToggle.setAttribute("aria-pressed", String(isDark));
    themeToggle.setAttribute(
        "aria-label",
        isDark ? "Switch to light mode" : "Switch to dark mode"
    );
}

let initialTheme = localStorage.getItem("theme");

if (initialTheme !== "dark" && initialTheme !== "light") {
    const prefersDark = window.matchMedia(
        "(prefers-color-scheme: dark)"
    ).matches;

    initialTheme = prefersDark ? "dark" : "light";

}

applyTheme(initialTheme);