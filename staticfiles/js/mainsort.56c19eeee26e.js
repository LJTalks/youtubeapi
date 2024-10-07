// Script for email obfuscation
document.getElementById('emailLink').addEventListener('click', function () {
    window.location.href = 'mailto:laura@ljtalks.com';
});

// Script for sorting
function sortBy(field, order) {
    const url = new URL(window.location.href);
    url.searchParams.set('sort_by', field);
    url.searchParams.set('order', order);
    window.location.href = url.href; // Trigger the page reload with the sorting parameters
}