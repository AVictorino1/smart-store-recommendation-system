import { useState, useEffect } from "react";
import styles from "./EditProductModal.module.css";
import { BsPencilSquare } from "react-icons/bs";
import { updateProductPartial } from "../../services/productService";

const EXCLUDED_FIELDS = ["id", "image_url"];
const PRIMARY_FIELDS = ["name", "price", "category", "subcategory", "brand", "color"];

function EditModal({ close, product }) {
    
    const [form, setForm] = useState({});
    const secondaryFields = Object.keys(form).filter(
    key => !EXCLUDED_FIELDS.includes(key) && !PRIMARY_FIELDS.includes(key)
    );
    const [changesMade, setChangesMade] = useState(false);
    const [showMore, setShowMore] = useState(false);
    console.log("secondary:", secondaryFields);
    useEffect(() => {
        if (product) {
            setForm(product);
        }
    }, [product]);

    function handleChange(e) {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
        setChangesMade(true);
    }

    async function handleSave(){
        try{
            await updateProductPartial(product.id,form); 
            setChangesMade(false);
        }catch(error){
                console.error(error);
            }
        }
            
        

    return (
    <div className={styles.overlay}>
        <div className={styles.modal}>
                     
            {form.image_url && (
                <div className={styles.imageContainer}>   
                    <img
                        src={form.image_url}
                        alt={form.name || "Producto"}
                        className={styles.image}
                    />
                    <div className={styles.imageOverlay}>
                        <BsPencilSquare className={styles.imageOverlayIcon} />
                    </div>

                </div>
            )}
            <div className={styles.rightPanel}>

            
                <div className={styles.header}>
                    <h2 className={styles.title}>
                        Editar producto
                    </h2>
                    
                </div>

                <div className={styles.content}>
                    
                        {PRIMARY_FIELDS.map(field => (
                            <div key={field} className={styles.formGroup}>
                                <label className={styles.label}>
                                    {field}
                                </label>

                                <input
                                    className={styles.input}
                                    name={field}
                                    value={form[field] || ""}
                                    onChange={handleChange}
                                />
                            </div>
                        ))}
                        {showMore && secondaryFields.map(field => (
                            <div key={field} className={styles.formGroup}>
                                <label className={styles.label}>
                                    {field}
                                </label>

                                <input
                                    className={styles.input}
                                    name={field}
                                    value={form[field] || ""}
                                    onChange={handleChange}
                                />
                            </div>
                        ))}

                    <button
                        type="button"
                            className={styles.showMoreButton}
                            onClick={() => setShowMore(!showMore)}>
                            {showMore ? "Mostrar menos": "Mostrar más"}
                    </button>
                        
                    <div className={styles.buttonContainer}>

                        <button
                            className={styles.closeButton}
                            onClick={close}
                        >
                            Cancelar
                        </button>
                        
                        <button
                            className={`${styles.saveButton} ${changesMade ? styles.saveButtonActive : ""}`}
                            onClick={handleSave}>
                            Guardar cambios
                        </button>



                    </div>

                </div>
            </div>
        </div>
    </div>
);}

export default EditModal;