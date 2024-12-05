document.addEventListener('DOMContentLoaded', () => {
    const quantityInputs = document.querySelectorAll('.basket-quantity');
    const checkoutButton = document.getElementById('checkout-button');

    const validateStock = () => {
        let hasStockIssues = false;

        quantityInputs.forEach(input => {
            const stock = parseInt(input.getAttribute('data-stock'));
            const quantity = parseInt(input.value);
            const warning = document.getElementById(`stock-warning-${input.getAttribute('data-item-id')}`);

            if (quantity > stock) {
                warning.style.display = 'block';
                hasStockIssues = true;
            } else {
                warning.style.display = 'none';
            }
        });

        checkoutButton.disabled = hasStockIssues;
    };


    const updateBasket = (itemId, newQuantity) => {
        return fetch('/update-basket-quantity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ item_id: itemId, quantity: newQuantity })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (!data.success) {
                alert('Failed to update the basket.');
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            alert('Failed to update the basket.');
        });
    };

    quantityInputs.forEach(input => {
        input.addEventListener('input', () => {
            const itemId = input.getAttribute('data-item-id');
            const newQuantity = parseInt(input.value);

            validateStock();

            const stock = parseInt(input.getAttribute('data-stock'));
            if (newQuantity <= stock) {
                updateBasket(itemId, newQuantity).then(() => {
                    location.reload();
                });
            }
        });
    });

    validateStock();

    const removeButtons = document.querySelectorAll('.remove-item');

    removeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const itemId = button.getAttribute('data-id');

            fetch('/remove-from-basket', {
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
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Failed to remove item.');
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                alert('Failed to remove item.');
            });
        });
    });
});