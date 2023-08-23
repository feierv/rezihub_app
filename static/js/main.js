window.addEventListener("DOMContentLoaded", () => {
    const main = document.querySelector('#main');

    const updateViewportHeight = () => {
        const viewportHeight = window.innerHeight;
        main.style.height = `${viewportHeight}px`;
    };

    updateViewportHeight();
    window.addEventListener("resize", updateViewportHeight);
});
