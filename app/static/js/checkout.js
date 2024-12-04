const stripe = Stripe('pk_test_51QS74ZFYg0cFbH8aFQyL5XpWeVNz8oSwJ3P0qYtrvFzL6fqCd2MvlS6S6NvjaaCqRhhyftx6kWJpQeYTr0OfmXde003pftoHD9');

document.getElementById('checkout-button').addEventListener('click', async () => {
    try {
        const response = await fetch('/checkout', { method: 'POST' });
        const { id } = await response.json();
        if (id) {
            stripe.redirectToCheckout({ sessionId: id });
        }
    } catch (error) {
        console.error('Error during checkout:', error);
        alert('Failed to initiate checkout. Please try again.');
    }
});