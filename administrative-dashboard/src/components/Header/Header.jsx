import NewProductButton from '../NewProductButton/NewProductButton.jsx'
import UserIcon from '../UserIcon/UserIcon.jsx'
import styles from './Header.module.css'
import SearchBar from '../SearchBar/SearchBar.jsx'
import { BsBoxSeam, BsClipboardCheck, BsBarChart, BsGear } from "react-icons/bs";
function Header(){
    return(
        <header className={styles.Header}>
            <div className={styles.topBar}>
                <h1>Administrative Dashboard</h1>
                <SearchBar></SearchBar>
                <UserIcon />
            </div>
            <nav className={styles.menu}>
                <div className={styles.newButtonWrapper}>
                    <NewProductButton />
                </div>
                <ul className={styles.main_dashboard}>  
                    <li><a href="#"><BsBoxSeam className={styles.navIcon} /> Inventario</a></li>
                    <li><a href="#"><BsClipboardCheck className={styles.navIcon} /> Pedidos</a></li>    
                    <li><a href="#"><BsBarChart className={styles.navIcon} /> Estadísticas</a></li>
                    <li><a href="#"><BsGear className={styles.navIcon} /> Configuración</a></li>  
                </ul>
            </nav>
        </header>
    );
}

export default Header