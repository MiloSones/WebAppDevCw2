document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.add-to-basket');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const itemId = button.getAttribute('product-id');

            fetch('/add-to-basket', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: itemId })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                alert('Failed to add item to basket.');
            });
        });
    });
});
