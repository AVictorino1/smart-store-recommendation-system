import styles from "./PopUpModal.module.css";
import { useState, useEffect } from "react";

function PopUpModalF({product, triggers, setForm, handleSave, close, handleSaveAnywayF, regeneratedFields, highlightIA}){
    const [iaButtonClicked, setIaButtonClicked] = useState(false);
    
    async function handleRegenerateWithAI(){
        const res = await fetch("http://localhost:8000/regenerate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(
                {
                    product: product,
                    fields: triggers
                }
            )
        });
        const data = await res.json();
        const data_id = {...data, id:product.id};
        handleSaveAnywayF(data_id);
        return data_id;
    }

    function isButtonIaActive(){
        return iaButtonClicked;
    }
    return(
    <div className={styles.popupOverlay}>
        <div className={styles.popup}>
            
            <h3 className={styles.popupTitle}>
                ¡Los cambios realizados afectan a otros campos!
            </h3>
            <p className={styles.popupMessage}>
                Los cambios que realizaste afectan a los siguientes campos: 
                <strong> {regeneratedFields.join(", ")}</strong>.
                ¿Qué querés hacer?
            </p>
            

            <div className={styles.popupButtons}>
                
                <button
                    className={`${isButtonIaActive() ? styles.popupButtonPrimaryActive : styles.popupButtonPrimary}`}
                    onClick={async() => {
                        setIaButtonClicked(true);
                        await handleRegenerateWithAI();
                        highlightIA();
                    }}
                >
                    Actualizar campos con IA
                </button>

                <button
                    className={styles.popupButtonSecondary}
                    onClick={handleSaveAnywayF}
                >
                    Guardar de todas formas
                </button>

                <button
                    className={styles.popupButtonDanger}
                    onClick={close}
                >
                    Cancelar
                </button>

            </div>
        </div>
    </div>);
}

export default PopUpModalF;

