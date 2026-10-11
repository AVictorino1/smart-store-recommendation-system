import { useState, useEffect } from "react";
import styles from "./EditProductModal.module.css";
import { BsPencilSquare } from "react-icons/bs";
import { updateProductPartial } from "../../services/productService";
import PopUpModalF from "../PopUp/PopUpModal";




const EXCLUDED_FIELDS = ["id", "image_url"];
const PRIMARY_FIELDS = ["name", "price", "category", "subcategory", "brand", "color"];

function EditModal({ close, product, onSave }) {
    
    const [form, setForm] = useState({});
    const [affectedFields, setAffectedFields] = useState([])  
    const [savedFields, setSavedFields] = useState([])  
    const [triggerFields, setTriggerFields] = useState([])
    const [regeneratedFields, setRegeneratedFields] = useState([])    
    const [error, setError] = useState(null)
    const [updatedIa, setUpdatedIa] = useState([]);
    const [showPopUp, setShowPopUp] = useState(false) 
    const [highlightedRegenerated, setHighlightedRegenerated] = useState([]);  
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
        const { name, value } = e.target;
        setForm({
            ...form,
            [name]: value
        });
        setChangesMade(true);

        // Si el usuario edita el campo que disparó el trigger, se quitan todos los highlights pendientes (trigger + regenerados)
        if (affectedFields.includes(name)) {
            setAffectedFields([]);
            setHighlightedRegenerated([]);
            setUpdatedIa([]);
        }

        // Si el usuario vuelve a tocar un campo ya marcado como guardado, se le quita esa marca
        if (savedFields.includes(name)) {
            setSavedFields(savedFields.filter(field => field !== name));
            setUpdatedIa([]);
            
        }
        if ((savedFields.includes(name) && triggerFields.includes(name)) || regeneratedFields.includes(name) ) {
            setSavedFields([]);
            setUpdatedIa([]);
            
        }
        // Si el usuario toca un campo actualizado con ia
        if(updatedIa.includes(name)){
            setUpdatedIa([]);
        }
    }
    
    function isFieldHighlighted(field) {
        return affectedFields.includes(field) || highlightedRegenerated.includes(field);
    }

    function isUpdatedIa(field){
        return updatedIa.includes(field);
    }

    async function handleSave(productToSave = form){
        console.log(productToSave);
        try{
            const changedFields = Object.keys(productToSave).filter(key => String(productToSave[key]).trim().toLowerCase() !== String(product[key]).trim().toLowerCase());
            const changedFieldsTrigger = changedFields.filter(field => triggerFields.includes(field));
            if (changedFieldsTrigger.length != 0){
                console.error('ERROR, CAMPOS AFECTADOS');
                setAffectedFields(changedFieldsTrigger);
                setHighlightedRegenerated(regeneratedFields);

                const allHighlighted = [...changedFieldsTrigger, ...regeneratedFields];
                if (allHighlighted.some(field => secondaryFields.includes(field))) {
                    setShowMore(true);
                }

                setShowPopUp(true);
                return;
            }
            setChangesMade(false);
            await updateProductPartial(product.id, productToSave); 
            setAffectedFields([]);
            setHighlightedRegenerated([]);
            setSavedFields(changedFields);
            onSave(productToSave);
        }catch(error){
                console.error(error);
            }
        }
    async function handleSaveAnyway(productToSave = form){
        try{
            const changedFields = Object.keys(productToSave).filter(key => String(productToSave[key]).trim().toLowerCase() !== String(product[key]).trim().toLowerCase());
            await updateProductPartial(product.id, productToSave); 
            setChangesMade(false);
            onSave(productToSave);
            setShowPopUp(false);
            setAffectedFields([]);
            setHighlightedRegenerated([]);
            setSavedFields(changedFields);
        }catch(error){
                console.error(error);
            }
        }
    useEffect(() => {
        fetch("http://localhost:8000/business/schema")
        .then(res => {
            if (!res.ok) throw new Error("Error al obtener información del negocio")
            return res.json()        
        }
        )

        .then(data => {
            setTriggerFields(JSON.parse(data['trigger_fields']))
            setRegeneratedFields(JSON.parse(data['regenerated_fields']))
            
        })
        .catch(err => {
            setError(err.message)
        })


    }, [])  
        

    return (
    <div className={styles.overlay}>
        <div className={styles.modal}>
            {showPopUp && <PopUpModalF product={form} triggers={affectedFields} setForm={setForm} handleSave={() => handleSave()} close={() => setShowPopUp(false)} handleSaveAnywayF = {(productToSave) => handleSaveAnyway(productToSave)} regeneratedFields={regeneratedFields} highlightIA = {() => setUpdatedIa(regeneratedFields)}></PopUpModalF>}   
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
                                    className={`${styles.input} ${isUpdatedIa(field) ? styles.inputUpdatedIa : ""} ${isFieldHighlighted(field) ? styles.inputHighlighted : ""} ${(savedFields.includes(field) && isUpdatedIa(field) == false) ? styles.inputSaved : ""}`}
                                    name={field}
                                    value={form[field] || ""}
                                    onChange={handleChange}
                                    onFocus={() => {setSavedFields([]);
                                        setUpdatedIa([]);}
                                    }
                                />

                                {affectedFields.includes(field) && (
                                    <p className={styles.fieldWarning}>
                                        El cambio realizado no fue guardado dado que afecta a otros campos
                                    </p>
                                )}

                                {(savedFields.includes(field) && isUpdatedIa(field) == false) && (
                                    <p className={styles.fieldSaved}>
                                        El cambio ha sido guardado
                                    </p>
                                )}
                                {(isUpdatedIa(field) == true) && (
                                    <p className={styles.fieldUpdatedIa}>
                                        ¡El campo ha sido actualizado con IA exitosamente!
                                    </p>
                                )}
                            </div>
                        ))}
                        {showMore && secondaryFields.map(field => (
                            <div key={field} className={styles.formGroup}>
                                <label className={styles.label}>
                                    {field}
                                </label>

                                <input
                                    className={`${styles.input} ${isUpdatedIa(field) ? styles.inputUpdatedIa : ""} ${isFieldHighlighted(field) ? styles.inputHighlighted : ""} ${(savedFields.includes(field) && isUpdatedIa(field) == false) ? styles.inputSaved : ""}`}
                                    name={field}
                                    value={form[field] || ""}
                                    onChange={handleChange}
                                    onFocus={() => {setSavedFields([]);
                                        setUpdatedIa([]);}
                                    }
                                />

                                {affectedFields.includes(field) && (
                                    <p className={styles.fieldWarning}>
                                        El cambio realizado no fue guardado dado que afecta a otros campos
                                    </p>
                                )}

                                {(savedFields.includes(field) && isUpdatedIa(field) == false) && (
                                    <p className={styles.fieldSaved}>
                                        El cambio ha sido guardado
                                    </p>
                                )}
                                {(isUpdatedIa(field) == true) && (
                                    <p className={styles.fieldUpdatedIa}>
                                        ¡El campo ha sido actualizado con IA exitosamente!
                                    </p>
                                )}
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
                            onClick={() => handleSave()}>
                            Guardar cambios
                        </button>
                        


                    </div>
                    
                </div>
            </div>
        </div>
        
    </div>
);}

export default EditModal;