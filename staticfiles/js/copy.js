//async function fetchProducts() {
//     try {
//         let response = await fetch("http://127.0.0.1:8000/products/"); // Adjust URL if necessary
//         let products = await response.json();

//         let productContainer = document.getElementById("product-list");
//         productContainer.innerHTML = ""; // Clear the loading message

//         if (products.length === 0) {
//             productContainer.innerHTML = "<p>No products available.</p>";
//         } else {
//             products.forEach(product => {
//                 let card = document.createElement("div");
//                 card.className = "product-card";
//                 card.innerHTML = `
//                     <h3>${product.name}</h3>
//                     <p>${product.description}</p>
//                     <p><strong>Price:</strong> $${product.price}</p>
//                     <p><strong>Stock:</strong> ${product.stock}</p>
//                 `;
//                 productContainer.appendChild(card);
//             });
//         }
//     } catch (error) {
//         console.error("Error fetching products:", error);
//         document.getElementById("product-list").innerHTML = "<p>Failed to load products.</p>";
//     }
// }

// fetchProducts();



// <
// section >
//     <
//     div class = "custom-shape-divider-bottom-1731247772" >
//     <
//     svg data - name = "Layer 1"
// xmlns = "http://www.w3.org/2000/svg"
// viewBox = "0 0 1200 120"
// preserveAspectRatio = "none" >
//     <
//     path d = "M985.66,92.83C906.67,72,823.78,31,743.84,14.19c-82.26-17.34-168.06-16.33-250.45.39-57.84,11.73-114,31.07-172,41.86A600.21,600.21,0,0,1,0,27.35V120H1200V95.8C1132.19,118.92,1055.71,111.31,985.66,92.83Z"
// class = "shape-fill" > < /path> < /
// svg > <
//     /div> < /
// section >