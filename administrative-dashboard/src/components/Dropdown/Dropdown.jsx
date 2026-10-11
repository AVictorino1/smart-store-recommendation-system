import { useState } from "react"
import styles from "./Dropdown.module.css"

function Dropdown({ label, options, onSelect, icon }) {
    const [open, setOpen] = useState(false)
    const [selected, setSelected] = useState(label)

    function handleSelect(option) {
        setSelected(option.label)
        onSelect(option.value)
        setOpen(false)
    }

    return (
        <div className={styles.wrapper}>
            <button
                onClick={() => setOpen(!open)}
                title={label}
                className={styles.trigger}
            >
                {icon ? icon : <span className={styles.label}>{selected}</span>}
                <span className={`${styles.arrow} ${open ? styles.arrowOpen : ""}`}></span>
            </button>

            {open && (
                <ul className={styles.menu}>
                    {options.map(option => (
                        <li
                            key={option.value}
                            onClick={() => handleSelect(option)}
                            className={styles.menuItem}
                        >
                            {option.label}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}

export default Dropdown