// SearchBar.jsx
import { FiSearch } from "react-icons/fi";
import styles from "./SearchBar.module.css";

function SearchBar({ placeholder = "Buscar" }) {
    return (
        <div className={styles.wrapper}>
            <div className={styles.searchBar}>
                <FiSearch className={styles.icon} />
                <input
                    type="text"
                    className={styles.input}
                    placeholder={placeholder}
                />
            </div>
        </div>
    );
}

export default SearchBar;