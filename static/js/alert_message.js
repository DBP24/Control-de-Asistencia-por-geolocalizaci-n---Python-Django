
document.addEventListener('DOMContentLoaded', function() {
    const toast = document.getElementById('toast-success');
    const closeButton = toast.querySelector('button');

    // Función para mostrar el toast
    const showToast = () => {
        toast.classList.remove('hidden');
        // Ocultar el toast después de 5 segundos
        setTimeout(() => {
            toast.classList.add('hidden');
        }, 4000);
    };

    // Mostrar el toast cuando la página se carga (si hay un mensaje para mostrar)
    showToast();

    // Función para cerrar el toast manualmente
    closeButton.addEventListener('click', () => {
        toast.classList.add('hidden');
    });
});
