import styles from './Card.module.css'

function Card({product_name = "Product name", product_description= "Product description", price= 0, isSold = false}){

    return(
        <div className={styles.card}>
            <img className={styles.card_image} src="https://placehold.co/150" alt="Product Image"></img>
            <h2>{product_name}</h2>
            <p>{product_description}</p>
            <p>{price}</p>
            <p className={styles.isSoldText}>{isSold ? "VENDIDO": "DISPONIBLE"}</p>
        </div>

    );
}


export default Card