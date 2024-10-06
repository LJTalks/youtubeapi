< script >
    function sortBy(field, order) {
        const url = new URL(window.location.href);
        url.searchParams.set('sort_by', field);
        url.searchParams.set('order', order);
        window.location.href = url.href; // Trigger the page reload with the sorting parameters
    } <
    /script>