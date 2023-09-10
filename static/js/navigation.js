const navLinks = [
    '/dashboard',
    '/learning/chapter-select',
    '/learning/learning-session'
];

const currentPath = window.location.pathname;
const navbarLinks = document.querySelectorAll('.navbar__link');

// Function to determine if a link should be active
function shouldLinkBeActive(link, path) {
    return path.startsWith(link);
}

// Loop through navbar links and add/remove active class
navbarLinks.forEach((link) => {
    const linkPath = link.getAttribute('href'); // Assuming your links have 'href' attributes
    if (shouldLinkBeActive(linkPath, currentPath) || currentPath.startsWith(linkPath + '/')) {
        link.classList.add('navbar__link--active');
    }
    else {
        link.classList.remove('navbar__link--active');
    }
});
