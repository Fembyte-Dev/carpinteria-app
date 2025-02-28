 // Funcionalidad para el sidebar
 document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    
    // Función para verificar si es móvil
    function isMobile() {
        return window.innerWidth < 992;
    }
    
    // Alternar sidebar
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('active');
        
        if (isMobile()) {
            // En móvil mostramos overlay
            if (sidebar.classList.contains('active')) {
                sidebarOverlay.style.display = 'block';
            } else {
                sidebarOverlay.style.display = 'none';
            }
        } else {
            // En escritorio ajustamos el margen del contenido
            mainContent.classList.toggle('sidebar-active');
        }
    });
    
    // Cerrar sidebar al hacer clic en el overlay (solo móvil)
    sidebarOverlay.addEventListener('click', function() {
        sidebar.classList.remove('active');
        sidebarOverlay.style.display = 'none';
    });
    
    // Ajustar el diseño basado en el tamaño de la ventana
    window.addEventListener('resize', function() {
        if (isMobile()) {
            mainContent.classList.remove('sidebar-active');
            if (sidebar.classList.contains('active')) {
                sidebarOverlay.style.display = 'block';
            }
        } else {
            sidebarOverlay.style.display = 'none';
            if (sidebar.classList.contains('active')) {
                mainContent.classList.add('sidebar-active');
            }
        }
    });
    
    // Manejo de Modal (solo como ejemplo)
    const modalExample = document.getElementById('modal-example');
    const modalClose = document.getElementById('modal-close');
    const modalCancel = document.getElementById('modal-cancel');
    
    if (modalClose) {
        modalClose.addEventListener('click', function() {
            modalExample.classList.remove('active');
        });
    }
    
    if (modalCancel) {
        modalCancel.addEventListener('click', function() {
            modalExample.classList.remove('active');
        });
    }
    
    // Para abrir el modal (ejemplo de uso)
    // document.getElementById('open-modal-btn').addEventListener('click', function() {
    //     modalExample.classList.add('active');
    // });
});