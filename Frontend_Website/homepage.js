function goToArrivals() {
    window.location.href = "New Arrivals.html"; 
}

// --- Cart Logic Functions ---

// Retrieves the cart array from local storage
function getCart() {
    const cartString = localStorage.getItem('shoppingCart');
    // If cart is found, parse it; otherwise, return an empty array
    return cartString ? JSON.parse(cartString) : [];
}

// Saves the current cart array to local storage
function saveCart(cart) {
    localStorage.setItem('shoppingCart', JSON.stringify(cart));
}

// Adds a new item or increments an existing one
function addToCart(id, name, price) {
    // Ensure price is treated as a number for calculations
    const itemPrice = parseFloat(price); 
    let cart = getCart();

    // Check if the item already exists in the cart
    let existingItem = cart.find(item => item.id.toString() === id.toString());

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: id,
            name: name,
            price: itemPrice,
            quantity: 1
        });
    }

    saveCart(cart);
    // Use template literals (backticks) for the alert message
    alert('added to cart');
}

// Function to display the cart items on the 'your cart.html' page
function displayCart() {
    const cart = getCart(); 
    const container = document.getElementById('cart-items-container');
    const totalItemsSpan = document.getElementById('total-items');
    const totalPriceSpan = document.getElementById('total-price');
    
    let totalItems = 0;
    let totalPrice = 0;

    // Clear any previous content in the container
    container.innerHTML = ''; 

    if (cart.length === 0) {
        container.innerHTML = '<p>Your shopping cart is empty. Go back to the <a href="homepage.html">Home Page</a> to start shopping!</p>';
        totalItemsSpan.textContent = 0;
        totalPriceSpan.textContent = '0.00';
        return; 
    }

    // Loop through each item to generate HTML and calculate totals
    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        totalItems += item.quantity;
        totalPrice += itemTotal;
        
        // Use a simple structure for displaying the item
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('cart-item');
        itemDiv.innerHTML = `
            <div class="cart-item-details">
                <h3>${item.name}</h3>
                <p>Price: ₹${item.price.toFixed(2)}</p>
                <p>Quantity: ${item.quantity}</p>
            </div>
            <div class="cart-item-summary">
                <strong>Subtotal: ₹${itemTotal.toFixed(2)}</strong>
                <button onclick="removeItem('${item.id}')">Remove</button>
            </div>
        `;
        container.appendChild(itemDiv);
    });

    // Update the summary section
    totalItemsSpan.textContent = totalItems;
    totalPriceSpan.textContent = totalPrice.toFixed(2);
}

// Function to remove an item (optional, but highly recommended)
function removeItem(id) {
    let cart = getCart();
    // Filter out the item with the matching ID
    cart = cart.filter(item => item.id.toString() !== id.toString());
    saveCart(cart); // Save the updated cart
    displayCart();  // Refresh the page display
}