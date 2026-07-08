export async function updateProductPartial(id,data){
    const response = await fetch(
        `http://localhost:8000/products/${id}`,
        {
            method:"PATCH",
            headers: {
                "Content-type":"application/JSON",
            },
            body: JSON.stringify(data)
        }
    )

    if (!response.ok){
        throw new Error("Error al actualizar producto");
    }

    return(response.json());
}