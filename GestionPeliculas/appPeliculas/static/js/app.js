function eliminarPelicula(id){
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡No podrás revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, borrarlo!'
    }).then((result) => {
        if (result.isConfirmed) {
            location.href = "/eliminarPelicula/" + id;
        }   
    })
}
