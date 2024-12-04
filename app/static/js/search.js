document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('search-bar');
    const productCards = document.querySelectorAll('.product-card');

    searchBar.addEventListener('input', () => {
        const searchTerm = searchBar.value.toLowerCase();

        productCards.forEach(card => {
            const title = card.getAttribute('data-title');
            const category = card.getAttribute('data-category');

            if (title.includes(searchTerm) || category.includes(searchTerm)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });
});