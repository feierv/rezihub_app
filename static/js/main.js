window.addEventListener("DOMContentLoaded", () => {
    const main = document.querySelector('#main');

    const updateViewportHeight = () => {
        const viewportHeight = window.innerHeight;
        main.style.minHeight = `${viewportHeight}px`;
    };

    updateViewportHeight();
    window.addEventListener("resize", updateViewportHeight);
});
