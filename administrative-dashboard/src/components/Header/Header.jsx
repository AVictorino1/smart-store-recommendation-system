import styles from './Header.module.css'
function Header(){

    return(
        <header className={styles.Header}>
            <h1>Administrative Dashboard</h1>
            <nav className={styles.menu}>
                <ul className={styles.main_dashboard}>  
                    <li><a href="#">Inventario</a></li>  
                    <li><a href="#">Estadísticas</a></li>
                    <li><a href="#">Configuración</a></li>  

                </ul>

            </nav>
            
        </header>


    );
}

export default Header