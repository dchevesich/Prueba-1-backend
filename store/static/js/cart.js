// store/static/js/cart.js
console.log("cart.js cargado y ejecutándose."); // Mensaje de depuración

var updateBtns = document.getElementsByClassName('update-cart'); // Selecciona todos los botones con la clase 'update-cart'
console.log('Número de botones "Add to Cart" encontrados:', updateBtns.length); // Mensaje de depuración

// Itera sobre cada botón y añade un 'event listener'
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product; // Obtiene el ID del producto del atributo data-product
        var action = this.dataset.action;     // Obtiene la acción (ej. 'add', 'remove') del atributo data-action
        console.log('productId:', productId, 'Action:', action);

        // Obtenemos el CSRF token de las cookies
        var csrftoken = getCookie('csrftoken');

        // Verifica si el usuario está logueado
        // user se define como una variable global en main.html
        if (user === 'AnonymousUser') {
            console.log('User is not authenticated. Cart items will not persist for anonymous users across browser sessions.');
            // Implementar lógica de carrito para usuarios anónimos (ej. en localStorage) aquí, si es necesario.
            // Por ahora, solo los usuarios logueados tienen persistencia en sesión.
            alert('Debes iniciar sesión para añadir ítems al carrito de forma persistente.');
        } else {
            updateUserOrder(productId, action, csrftoken); // Llama a la función que enviará la solicitud al backend
        }
    });
}

// Función para obtener el CSRF token de las cookies (código estándar de Django)
function getCookie(name) {
    var cookieArr = document.cookie.split(";");
    for (var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        if (name == cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

// Función que envía la solicitud al backend
function updateUserOrder(productId, action, csrftoken) {
    console.log('Sending data...');

    var url = '/update_item/'; // La URL de tu vista updateItem en Django

    fetch(url, {
        method: 'POST', // Es una solicitud POST
        headers: {
            'Content-Type': 'application/json', // Indicamos que enviamos JSON
            'X-CSRFToken': csrftoken,          // Enviamos el CSRF token por seguridad
        },
        body: JSON.stringify({ 'productId': productId, 'action': action }) // Enviamos el ID del producto y la acción como JSON
    })
        .then((response) => {
            // Verifica si la respuesta es OK (status 2xx)
            if (!response.ok) {
                // Si la respuesta no es OK, lanza un error con el status para el catch
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json(); // Parsea la respuesta JSON del servidor
        })
        .then((data) => {
            console.log('data:', data);
            location.reload(); // Recarga la página para mostrar el carrito actualizado (esto es básico, luego se puede mejorar)
        })
        .catch((error) => {
            console.error('Error al actualizar el carrito:', error);
            alert('Ocurrió un error al añadir/remover el ítem del carrito. Por favor, inténtalo de nuevo.');
        });
}