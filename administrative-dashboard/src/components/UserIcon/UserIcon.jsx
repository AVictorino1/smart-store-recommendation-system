// UserIcon.jsx
import { FaUserCircle } from "react-icons/fa";
import styles from "./UserIcon.module.css";

function UserIcon() {
    return (
        <div className={styles.userIcon}>
            <FaUserCircle className={styles.icon} />
        </div>
    );
}

export default UserIcon;