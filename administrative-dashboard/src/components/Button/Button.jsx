import styles from './Button.module.css'

function Button(){
    function clickHandler(e){
        console.log(e.className);
    }
    return(<><button className={styles.upload} onClick={(e) => clickHandler(e)}> Upload</button><br></br></>);
}

export default Button