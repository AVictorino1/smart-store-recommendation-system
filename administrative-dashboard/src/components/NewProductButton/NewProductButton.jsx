// NewProductButton.jsx
import { FiPlus } from "react-icons/fi";
import styles from "./NewProductButton.module.css";

function NewProductButton() {
    return (
        <button className={styles.newButton}>
            <FiPlus className={styles.icon} />
            <span>Nuevo Producto</span>
        </button>
    );
}

export default NewProductButton;